import time
import logging
from typing import Optional, Dict, Any, List
import httpx
from config import settings

logger = logging.getLogger("Portal.JITSync")

class JITSyncService:
    def __init__(self):
        self._admin_token: Optional[str] = None
        self._admin_token_expires_at: float = 0.0

    async def get_admin_token(self) -> str:
        """
        Obtains or refreshes the Keycloak admin-cli token.
        """
        now = time.time()
        if self._admin_token and now < (self._admin_token_expires_at - 30):
            return self._admin_token

        token_url = f"{settings.KEYCLOAK_INTERNAL_URL}/realms/master/protocol/openid-connect/token"
        data = {
            "client_id": "admin-cli",
            "username": settings.KEYCLOAK_ADMIN_USER,
            "password": settings.KEYCLOAK_ADMIN_PASSWORD,
            "grant_type": "password"
        }
        headers = {"User-Agent": "NigiriPortal-JIT/1.0"}

        async with httpx.AsyncClient(verify=False, timeout=10.0, headers=headers) as client:
            resp = await client.post(token_url, data=data)
            if resp.status_code != 200:
                logger.error(f"Failed to obtain Keycloak admin token: {resp.status_code} {resp.text}")
                raise RuntimeError(f"Keycloak admin authentication failed: {resp.status_code}")

            payload = resp.json()
            self._admin_token = payload["access_token"]
            self._admin_token_expires_at = now + payload.get("expires_in", 60)
            return self._admin_token

    async def get_user_discord_info(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieves user federated identities from Keycloak to find Discord ID.
        """
        token = await self.get_admin_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "NigiriPortal-JIT/1.0"
        }
        url = f"{settings.KEYCLOAK_INTERNAL_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}/federated-identity"

        async with httpx.AsyncClient(verify=False, headers=headers, timeout=10.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                feds = resp.json()
                for fed in feds:
                    if fed.get("identityProvider") == "discord":
                        return {
                            "linked": True,
                            "discord_id": str(fed.get("userId")),
                            "discord_username": fed.get("userName")
                        }
        return {"linked": False, "discord_id": None, "discord_username": None}

    async def check_discord_member_role(self, discord_user_id: str) -> Dict[str, Any]:
        """
        Directly checks Discord REST API for target guild membership and role.
        """
        url = f"https://discord.com/api/v10/guilds/{settings.DISCORD_SERVER_ID}/members/{discord_user_id}"
        headers = {
            "Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}",
            "User-Agent": "NigiriPortal-JIT/1.0"
        }

        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                member_roles = [str(r) for r in data.get("roles", [])]
                has_role = str(settings.DISCORD_ROLE_ID) in member_roles
                nickname = data.get("nick") or (data.get("user", {}) or {}).get("username")
                return {
                    "in_guild": True,
                    "has_role": has_role,
                    "nickname": nickname,
                    "roles": member_roles
                }
            elif resp.status_code == 404:
                return {
                    "in_guild": False,
                    "has_role": False,
                    "nickname": None,
                    "roles": []
                }
            else:
                logger.error(f"Discord API returned unexpected status {resp.status_code}: {resp.text}")
                return {
                    "in_guild": False,
                    "has_role": False,
                    "error": f"Discord API HTTP {resp.status_code}"
                }

    async def get_user_roles(self, user_id: str) -> List[str]:
        """
        Retrieves user realm roles from Keycloak.
        """
        token = await self.get_admin_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "NigiriPortal-JIT/1.0"
        }
        url = f"{settings.KEYCLOAK_INTERNAL_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}/role-mappings/realm"

        async with httpx.AsyncClient(verify=False, headers=headers, timeout=10.0) as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                return [r.get("name") for r in resp.json() if r.get("name")]
        return []

    async def ensure_developer_role(self, user_id: str) -> bool:
        """
        Assigns the 'Developer' realm role to user in Keycloak if not already present.
        """
        token = await self.get_admin_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "NigiriPortal-JIT/1.0"
        }

        # Check existing roles first
        existing_roles = await self.get_user_roles(user_id)
        if "Developer" in existing_roles:
            return True

        # Fetch Developer role representation
        role_url = f"{settings.KEYCLOAK_INTERNAL_URL}/admin/realms/{settings.KEYCLOAK_REALM}/roles/Developer"
        async with httpx.AsyncClient(verify=False, headers=headers, timeout=10.0) as client:
            resp = await client.get(role_url)
            if resp.status_code != 200:
                logger.error(f"Failed to fetch Developer role from Keycloak: {resp.status_code} {resp.text}")
                return False
            role_obj = resp.json()

            # Assign role
            assign_url = f"{settings.KEYCLOAK_INTERNAL_URL}/admin/realms/{settings.KEYCLOAK_REALM}/users/{user_id}/role-mappings/realm"
            resp_assign = await client.post(assign_url, json=[role_obj])
            if resp_assign.status_code in (200, 204):
                logger.info(f"Successfully assigned Developer role to Keycloak user {user_id}")
                return True
            else:
                logger.error(f"Failed to assign role to Keycloak user {user_id}: {resp_assign.status_code} {resp_assign.text}")
                return False

    async def sync_user(self, user_id: str) -> Dict[str, Any]:
        """
        Runs complete JIT sync workflow for a given Keycloak user ID.
        """
        if not user_id:
            return {
                "success": False,
                "reason": "no_user_id",
                "message": "ユーザー識別子（sub）が存在しません。"
            }

        try:
            # 1. Check if user already has Developer role in Keycloak
            roles = await self.get_user_roles(user_id)
            if "Developer" in roles:
                return {
                    "success": True,
                    "reason": "already_granted",
                    "message": "すでに開発者権限（Developer）が付与されています。",
                    "roles": roles
                }

            # 2. Check Discord federated identity
            d_info = await self.get_user_discord_info(user_id)
            if not d_info.get("linked") or not d_info.get("discord_id"):
                return {
                    "success": False,
                    "reason": "discord_not_linked",
                    "message": "OmusuBI アカウントに Discord アカウントが連携されていません。",
                    "discord_info": d_info
                }

            # 3. Check membership & role on Discord
            d_status = await self.check_discord_member_role(d_info["discord_id"])
            if not d_status.get("in_guild"):
                return {
                    "success": False,
                    "reason": "not_in_guild",
                    "message": "開発者 Discord サーバー（CLN Tokyo Tutors）に参加していません。",
                    "discord_info": d_info,
                    "guild_status": d_status
                }

            if not d_status.get("has_role"):
                return {
                    "success": False,
                    "reason": "missing_role",
                    "message": "Discord サーバーに参加していますが、開発者ロールが付与されていません。",
                    "discord_info": d_info,
                    "guild_status": d_status
                }

            # 4. Grant Developer role in Keycloak
            granted = await self.ensure_developer_role(user_id)
            if granted:
                return {
                    "success": True,
                    "reason": "newly_granted",
                    "message": "Discord 連携とロールを確認し、OmusuBI 開発者ロール（Developer）を付与しました！",
                    "discord_info": d_info,
                    "guild_status": d_status
                }
            else:
                return {
                    "success": False,
                    "reason": "keycloak_assign_error",
                    "message": "Keycloak への開発者ロール反映に失敗しました。",
                    "discord_info": d_info,
                    "guild_status": d_status
                }

        except Exception as e:
            logger.exception(f"Unexpected error during JIT sync for {user_id}: {e}")
            return {
                "success": False,
                "reason": "system_error",
                "message": f"同期処理中にエラーが発生しました: {str(e)}"
            }

jit_sync_service = JITSyncService()
