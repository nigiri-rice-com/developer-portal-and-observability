import os
import json
import time
import hmac
import hashlib
import base64
import urllib.parse
from pathlib import Path
from typing import Optional, List, Dict, Any

import httpx
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from jose import jwt

from config import settings
from jit_sync import jit_sync_service
from services_data import get_service_detail, get_all_services_list, SERVICES_DATA, OVERALL_MERMAID
import docs_data
from status_data import get_status_page_data

app = FastAPI(title="Nigiri Developer Portal", docs_url=None, redoc_url=None)

@app.middleware("http")
async def process_proxy_headers(request: Request, call_next):
    proto = request.headers.get("x-forwarded-proto")
    if proto:
        request.scope["scheme"] = proto
    return await call_next(request)


# Static files directory
static_dir = Path(__file__).resolve().parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)

@app.api_route("/static/{file_path:path}", methods=["GET", "HEAD"])
@app.api_route("/portal/static/{file_path:path}", methods=["GET", "HEAD"])
async def serve_static_files(file_path: str):
    try:
        candidate = (static_dir / urllib.parse.unquote(file_path)).resolve()
        if candidate.is_relative_to(static_dir) and candidate.is_file():
            return FileResponse(str(candidate))
    except Exception:
        pass
    raise HTTPException(status_code=404, detail="Static file not found")

# Mount templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Ensure data dir and default credentials exist
os.makedirs(os.path.dirname(settings.CREDENTIALS_PATH), exist_ok=True)
if not os.path.exists(settings.CREDENTIALS_PATH):
    with open(settings.CREDENTIALS_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

def load_credentials() -> List[Dict[str, Any]]:
    try:
        with open(settings.CREDENTIALS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_credentials(creds: List[Dict[str, Any]]):
    with open(settings.CREDENTIALS_PATH, "w", encoding="utf-8") as f:
        json.dump(creds, f, ensure_ascii=False, indent=2)

# --- Cookie Session Helper ---
def create_session_token(data: dict) -> str:
    payload = json.dumps(data)
    b64_payload = base64.urlsafe_b64encode(payload.encode()).decode()
    sig = hmac.new(settings.SESSION_SECRET.encode(), b64_payload.encode(), hashlib.sha256).hexdigest()
    return f"{b64_payload}.{sig}"

def verify_session_token(token: str) -> Optional[dict]:
    if not token or "." not in token:
        return None
    try:
        b64_payload, sig = token.split(".", 1)
        expected_sig = hmac.new(settings.SESSION_SECRET.encode(), b64_payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = base64.urlsafe_b64decode(b64_payload.encode()).decode()
        return json.loads(payload)
    except Exception:
        return None

def get_current_user(request: Request) -> Optional[dict]:
    token = request.cookies.get(settings.SESSION_COOKIE_NAME)
    return verify_session_token(token)

def get_base_url_for_request(request: Request) -> str:
    host = request.headers.get("x-forwarded-host") or request.headers.get("host") or "www.nigiri-rice.com"
    proto = request.headers.get("x-forwarded-proto") or "https"
    
    if "portal.nigiri-rice.com" in host or "dev.nigiri-rice.com" in host:
        return f"{proto}://{host}"
        
    return f"{proto}://{host}/portal"

# --- Tool Directory Definition ---
TOOLS_DATA = get_all_services_list()


INFRA_DATA = [
    {
        "name": "VPS メインホスト (nigiri-vps)",
        "description": "公開IP: 210.131.211.17 / SSH Port 22 (公開鍵認証)",
        "ip": "210.131.211.17",
        "port": "22",
        "command": "ssh root@210.131.211.17",
        "type": "SSH"
    },
    {
        "name": "Kubernetes クラスター (k3s)",
        "description": "5ノード構成 (ControlPlane 1 + Worker 4) / Pod: 10.42.0.0/16, Svc: 10.43.0.0/16",
        "ip": "10.43.0.1",
        "port": "443 / 6443",
        "command": "kubectl get nodes -o wide",
        "type": "K8s"
    },
    {
        "name": "OmusuBI Core PostgreSQL (内部)",
        "description": "Keycloak 認証ストア / コネクションプール上限 250 / 自動日次バックアップ (03:00 JST)",
        "ip": "omusubi-core-postgres.omusubi.svc.cluster.local",
        "port": "5432",
        "command": "psql -h omusubi-core-postgres.omusubi.svc.cluster.local -U keycloak -d keycloak",
        "type": "Database"
    },
    {
        "name": "WordPress MariaDB (内部)",
        "description": "nigiri-rice.com ホームページ用データベース / ローカルボリューム永続化",
        "ip": "mariadb.nigiri-homepage.svc.cluster.local",
        "port": "3306",
        "command": "mysql -h mariadb.nigiri-homepage.svc.cluster.local -u wordpress -p wordpress",
        "type": "Database"
    },
    {
        "name": "Ingress-NGINX コントローラー (NodePort)",
        "description": "エッジ Caddy からの内部ルーティング受け口 / HA 2 Pods 冗長稼働",
        "ip": "127.0.0.1 (VPS Host)",
        "port": "30180 (HTTP) / 30444 (HTTPS)",
        "command": "curl -I http://127.0.0.1:30180/healthz",
        "type": "Network"
    }
]

# --- Routes ---

@app.api_route("/healthz", methods=["GET", "HEAD"])
async def healthz():
    return {"status": "ok", "time": time.time()}

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def home_page(request: Request):
    user = get_current_user(request)
    base_url = get_base_url_for_request(request)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "base_url": base_url,
                "title": "Nigiri Developer Portal"
            }
        )

    # JIT Role Check & Auto-grant triggered by opening the developer portal
    sync_result = None
    if not user.get("is_developer") and not user.get("is_admin"):
        try:
            sync_result = await jit_sync_service.sync_user(user.get("sub"))
            if sync_result.get("success"):
                user["is_developer"] = True
                if "Developer" not in user.get("roles", []):
                    user.setdefault("roles", []).append("Developer")
                # Re-issue updated session cookie immediately
                new_session_token = create_session_token(user)
                credentials = load_credentials()
                resp = templates.TemplateResponse(
                    "index.html",
                    {
                        "request": request,
                        "user": user,
                        "tools": TOOLS_DATA,
                        "infra": INFRA_DATA,
                        "credentials": credentials,
                        "base_url": base_url,
                        "title": "Nigiri 開発者ポータル",
                        "just_synced": True
                    }
                )
                resp.set_cookie(
                    key=settings.SESSION_COOKIE_NAME,
                    value=new_session_token,
                    max_age=86400 * 7,
                    httponly=True,
                    samesite="lax",
                    secure=True
                )
                return resp
        except Exception as e:
            sync_result = {"success": False, "message": f"同期エラー: {e}"}

    if not user.get("is_developer") and not user.get("is_admin"):
        return templates.TemplateResponse(
            "denied.html",
            {
                "request": request,
                "user": user,
                "base_url": base_url,
                "sync_result": sync_result,
                "title": "アクセス権限が必要です"
            }
        )

    credentials = load_credentials()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
            "tools": TOOLS_DATA,
            "infra": INFRA_DATA,
            "overall_mermaid": OVERALL_MERMAID,
            "credentials": credentials,
            "base_url": base_url,
            "title": "Nigiri 開発者ポータル"
        }
    )

@app.api_route("/services/{service_id}", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route("/services/{service_id}/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def service_detail_page(service_id: str, request: Request):
    user = get_current_user(request)
    base_url = get_base_url_for_request(request)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "base_url": base_url,
                "title": "Nigiri Developer Portal"
            }
        )

    # JIT Role Check & Auto-grant
    if not user.get("is_developer") and not user.get("is_admin"):
        try:
            sync_result = await jit_sync_service.sync_user(user.get("sub"))
            if sync_result.get("success"):
                user["is_developer"] = True
                if "Developer" not in user.get("roles", []):
                    user.setdefault("roles", []).append("Developer")
        except Exception:
            pass

    if not user.get("is_developer") and not user.get("is_admin"):
        return templates.TemplateResponse(
            "denied.html",
            {
                "request": request,
                "user": user,
                "base_url": base_url,
                "title": "アクセス権限が必要です"
            }
        )

    service = get_service_detail(service_id)
    if not service:
        return RedirectResponse(url=f"{base_url}/", status_code=status.HTTP_302_FOUND)

    # Filter matching credentials for this service
    all_creds = load_credentials()
    keyword = service.get("cred_keyword", service_id).lower()
    matched_creds = []
    for c in all_creds:
        haystack = f"{c.get('title', '')} {c.get('category', '')} {c.get('description', '')} {c.get('identifier', '')}".lower()
        if keyword in haystack or service_id.lower() in haystack or service.get("name", "").lower() in haystack:
            matched_creds.append(c)

    return templates.TemplateResponse(
        "service_detail.html",
        {
            "request": request,
            "user": user,
            "service": service,
            "matched_creds": matched_creds,
            "base_url": base_url,
            "title": f"{service.get('name')} - サービス詳細 & 構成図"
        }
    )

# --- Documentation Routes (GitHub Docs Style) ---
 
@app.api_route("/docs", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route("/docs/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def docs_root(request: Request):
    base_url = get_base_url_for_request(request)
    return RedirectResponse(url=f"{base_url}/docs/overview", status_code=status.HTTP_302_FOUND)

@app.api_route("/docs/{doc_id}", methods=["GET", "HEAD"], response_class=HTMLResponse)
@app.api_route("/docs/{doc_id}/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def doc_page(doc_id: str, request: Request):
    user = get_current_user(request)
    base_url = get_base_url_for_request(request)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "base_url": base_url,
                "title": "Nigiri Developer Portal"
            }
        )

    # JIT Role Check & Auto-grant
    if not user.get("is_developer") and not user.get("is_admin"):
        try:
            sync_result = await jit_sync_service.sync_user(user.get("sub"))
            if sync_result.get("success"):
                user["is_developer"] = True
                if "Developer" not in user.get("roles", []):
                    user.setdefault("roles", []).append("Developer")
        except Exception:
            pass

    if not user.get("is_developer") and not user.get("is_admin"):
        return templates.TemplateResponse(
            "denied.html",
            {
                "request": request,
                "user": user,
                "base_url": base_url,
                "title": "アクセス権限が必要です"
            }
        )

    doc = docs_data.get_doc(doc_id)
    if not doc:
        return RedirectResponse(url=f"{base_url}/docs/overview", status_code=status.HTTP_302_FOUND)

    tree = docs_data.get_docs_tree()

    return templates.TemplateResponse(
        "docs.html",
        {
            "request": request,
            "user": user,
            "doc": doc,
            "tree": tree,
            "base_url": base_url,
            "title": f"{doc.get('title')} - Nigiri Docs"
        }
    )

# --- Public Statuspage Routes (Atlassian Statuspage Style) ---

@app.api_route("/status", methods=["GET", "HEAD"])
@app.api_route("/status/", methods=["GET", "HEAD"])
async def status_page(request: Request):
    return RedirectResponse(url="https://status.nigiri-rice.com", status_code=status.HTTP_302_FOUND)


@app.api_route("/api/status", methods=["GET", "HEAD"])
@app.api_route("/api/status/", methods=["GET", "HEAD"])
async def api_status_json():
    # Public JSON API
    return JSONResponse(content=get_status_page_data())

@app.api_route("/auth/login", methods=["GET", "HEAD"])
@app.api_route("/auth/login/", methods=["GET", "HEAD"])
async def auth_login(request: Request):
    base_url = get_base_url_for_request(request)
    redirect_uri = f"{base_url}/auth/callback"
    
    # Generate state
    state = base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
    
    auth_params = {
        "client_id": settings.OIDC_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email roles",
        "redirect_uri": redirect_uri,
        "state": state
    }
    
    auth_url = f"{settings.KEYCLOAK_PUBLIC_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth?{urllib.parse.urlencode(auth_params)}"
    
    resp = RedirectResponse(url=auth_url, status_code=status.HTTP_302_FOUND)
    resp.set_cookie(key="portal_state", value=state, max_age=300, httponly=True, samesite="lax", secure=True)
    return resp

@app.api_route("/auth/callback", methods=["GET", "HEAD"])
async def auth_callback(request: Request, code: Optional[str] = None, state: Optional[str] = None, error: Optional[str] = None):
    base_url = get_base_url_for_request(request)
    if error:
        return HTMLResponse(f"<h3>認証エラー</h3><p>{error}</p><a href='{base_url}'>ポータルトップへ</a>", status_code=400)
    
    if not code:
        raise HTTPException(status_code=400, detail="認証コードが見つかりません。")

    redirect_uri = f"{base_url}/auth/callback"

    # Token request
    token_url_internal = f"{settings.KEYCLOAK_INTERNAL_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
    token_url_public = f"{settings.KEYCLOAK_PUBLIC_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

    token_data = {
        "grant_type": "authorization_code",
        "client_id": settings.OIDC_CLIENT_ID,
        "client_secret": settings.OIDC_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri
    }

    tokens = None
    async with httpx.AsyncClient(verify=False, timeout=10.0) as client:
        try:
            r = await client.post(token_url_internal, data=token_data)
            if r.status_code == 200:
                tokens = r.json()
        except Exception:
            pass

        if not tokens:
            try:
                r = await client.post(token_url_public, data=token_data)
                if r.status_code == 200:
                    tokens = r.json()
                else:
                    raise HTTPException(status_code=400, detail=f"Token exchange failed: {r.text}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"OIDC Token Request Error: {e}")

    # Extract user info
    id_token = tokens.get("id_token")
    access_token = tokens.get("access_token")

    claims = {}
    if id_token:
        claims = jwt.get_unverified_claims(id_token)
    elif access_token:
        claims = jwt.get_unverified_claims(access_token)

    access_claims = {}
    if access_token:
        try:
            access_claims = jwt.get_unverified_claims(access_token)
        except Exception:
            pass

    roles = access_claims.get("realm_access", {}).get("roles", [])
    if not roles:
        roles = claims.get("realm_access", {}).get("roles", [])

    is_admin = "admin" in roles or "manage-realm" in roles
    is_developer = "Developer" in roles or is_admin

    # JIT Sync during OIDC login
    if not is_developer and claims.get("sub"):
        try:
            sync_res = await jit_sync_service.sync_user(claims.get("sub"))
            if sync_res.get("success"):
                is_developer = True
                if "Developer" not in roles:
                    roles.append("Developer")
        except Exception:
            pass

    user_info = {
        "sub": claims.get("sub"),
        "username": claims.get("preferred_username") or claims.get("sub"),
        "name": claims.get("name") or claims.get("preferred_username") or "Developer",
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "email": claims.get("email"),
        "picture": claims.get("picture"),
        "roles": roles,
        "is_developer": is_developer,
        "is_admin": is_admin
    }

    session_token = create_session_token(user_info)

    target_redirect = base_url if base_url else "/"
    resp = RedirectResponse(url=target_redirect, status_code=status.HTTP_302_FOUND)
    resp.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=session_token,
        max_age=86400 * 7,
        httponly=True,
        samesite="lax",
        secure=True
    )
    return resp

@app.post("/api/sync-discord")
async def api_sync_discord(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="ログインしていません。")

    sub = user.get("sub")
    res = await jit_sync_service.sync_user(sub)
    if res.get("success"):
        user["is_developer"] = True
        if "Developer" not in user.get("roles", []):
            user.setdefault("roles", []).append("Developer")
        new_token = create_session_token(user)
        response = JSONResponse(content=res)
        response.set_cookie(
            key=settings.SESSION_COOKIE_NAME,
            value=new_token,
            max_age=86400 * 7,
            httponly=True,
            samesite="lax",
            secure=True
        )
        return response
    return JSONResponse(content=res)

@app.api_route("/auth/logout", methods=["GET", "HEAD"])
@app.api_route("/auth/logout/", methods=["GET", "HEAD"])
async def auth_logout(request: Request):
    base_url = get_base_url_for_request(request)
    logout_url = (
        f"{settings.KEYCLOAK_PUBLIC_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/logout"
        f"?client_id={settings.OIDC_CLIENT_ID}"
        f"&post_logout_redirect_uri={urllib.parse.quote(base_url)}"
    )
    resp = RedirectResponse(url=logout_url)
    resp.delete_cookie(settings.SESSION_COOKIE_NAME)
    return resp

@app.api_route("/vault", methods=["GET", "HEAD"])
@app.api_route("/vault/", methods=["GET", "HEAD"])
@app.api_route("/credentials", methods=["GET", "HEAD"])
@app.api_route("/credentials/", methods=["GET", "HEAD"])
async def redirect_to_vault():
    return RedirectResponse(url="https://vault.nigiri-rice.com/ui/vault/auth?with=oidc", status_code=status.HTTP_302_FOUND)


class CredentialItem(BaseModel):
    title: str
    category: str
    identifier: str
    secret: str
    description: Optional[str] = ""

@app.post("/api/credentials/add")
async def add_credential(item: CredentialItem, request: Request):
    user = get_current_user(request)
    if not user or not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="管理者権限が必要です。")

    creds = load_credentials()
    new_id = f"cred-{int(time.time())}"
    new_item = {
        "id": new_id,
        "title": item.title.strip(),
        "category": item.category.strip(),
        "identifier": item.identifier.strip(),
        "secret": item.secret.strip(),
        "description": item.description.strip()
    }
    creds.append(new_item)
    save_credentials(creds)
    return {"success": True, "item": new_item}

@app.delete("/api/credentials/{item_id}")
async def delete_credential(item_id: str, request: Request):
    user = get_current_user(request)
    if not user or not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="管理者権限が必要です。")

    creds = load_credentials()
    creds = [c for c in creds if c.get("id") != item_id]
    save_credentials(creds)
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=False)
