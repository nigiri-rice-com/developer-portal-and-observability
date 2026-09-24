import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KEYCLOAK_INTERNAL_URL: str = os.getenv("KEYCLOAK_INTERNAL_URL", "http://omusubi-core.omusubi.svc.cluster.local:8080")
    KEYCLOAK_PUBLIC_URL: str = os.getenv("KEYCLOAK_PUBLIC_URL", "https://sso.nigiri-rice.com")
    KEYCLOAK_REALM: str = os.getenv("KEYCLOAK_REALM", "master")
    OIDC_CLIENT_ID: str = os.getenv("OIDC_CLIENT_ID", "nigiri-developer-portal")
    OIDC_CLIENT_SECRET: str = os.getenv("OIDC_CLIENT_SECRET", "oR28UjbCqmuyipEQWRvcFHZM0o28NtQJiBvrMIrj8ifQzt173gSloYWcupa9wk7FpxExMOqRDRGLzMkGGjwJfe")
    
    # Base URL for callbacks (can be dynamically determined or overridden)
    PUBLIC_BASE_URL: str = os.getenv("PUBLIC_BASE_URL", "https://www.nigiri-rice.com/portal")
    
    SESSION_SECRET: str = os.getenv("SESSION_SECRET", "nigiri-secret-portal-session-salt-2026")
    SESSION_COOKIE_NAME: str = "nigiri_portal_session"
    
    CREDENTIALS_PATH: str = os.getenv("CREDENTIALS_PATH", "/app/data/credentials.json")
    
    PORT: int = int(os.getenv("PORT", "8080"))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Keycloak Admin Credentials for JIT Role Provisioning
    KEYCLOAK_ADMIN_USER: str = os.getenv("KEYCLOAK_ADMIN_USER", "admin")
    KEYCLOAK_ADMIN_PASSWORD: str = os.getenv("KEYCLOAK_ADMIN_PASSWORD", "")

    # Discord Bot & Role Verification
    DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN", "")
    DISCORD_SERVER_ID: str = os.getenv("DISCORD_SERVER_ID", "")
    DISCORD_ROLE_ID: str = os.getenv("DISCORD_ROLE_ID", "")
    DISCORD_INVITE_URL: str = os.getenv("DISCORD_INVITE_URL", "https://discord.gg/example")

settings = Settings()
