"""Auth service — local login + OIDC callback + current-user resolution."""
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.db.models.auth import Enrolment, User, UserAuthProvider, UserStatus
from src.lib.exceptions import unauthorized
from src.lib.jwt import create_access_token, verify_password


async def authenticate_local(db: AsyncSession, email: str, password: str) -> tuple[str, int]:
    """Verify local credentials; return (access_token, expires_in)."""
    result = await db.execute(
        select(User).where(
            User.email == email.lower(),
            User.auth_provider == UserAuthProvider.local,
            User.deleted_at.is_(None),
        )
    )
    user = result.scalar_one_or_none()
    if user is None or not user.password_hash or not verify_password(password, user.password_hash):
        raise unauthorized("Invalid email or password.")
    if user.status != UserStatus.active:
        raise unauthorized("Account is not active.")
    return create_access_token(user.id, user.organization_id, user.global_role.value)


async def exchange_oidc_code(db: AsyncSession, code: str, state: str) -> tuple[str, int]:
    """Exchange OIDC authorization code for tokens; upsert user; return JWT."""
    token_url = f"{settings.oidc_issuer}/token"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.oidc_redirect_uri,
                "client_id": settings.oidc_client_id,
                "client_secret": settings.oidc_client_secret,
            },
        )
    if resp.status_code != 200:
        raise unauthorized("OIDC token exchange failed.")

    id_token_data = resp.json()
    userinfo = await _fetch_oidc_userinfo(id_token_data.get("access_token", ""))

    sub = userinfo.get("sub")
    email = userinfo.get("email", "").lower()
    display_name = userinfo.get("name", email)

    result = await db.execute(
        select(User).where(
            User.external_subject == sub,
            User.auth_provider == UserAuthProvider.oidc,
            User.deleted_at.is_(None),
        )
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise unauthorized("No Mahir account found for this SSO identity. Contact your org admin.")
    if user.status != UserStatus.active:
        raise unauthorized("Account is not active.")

    user.display_name = display_name
    await db.flush()
    return create_access_token(user.id, user.organization_id, user.global_role.value)


async def _fetch_oidc_userinfo(access_token: str) -> dict:
    userinfo_url = f"{settings.oidc_issuer}/userinfo"
    async with httpx.AsyncClient() as client:
        resp = await client.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})
    if resp.status_code != 200:
        raise unauthorized("Could not fetch OIDC userinfo.")
    return resp.json()


async def get_me(db: AsyncSession, user: User) -> dict:
    result = await db.execute(
        select(Enrolment).where(
            Enrolment.user_id == user.id,
            Enrolment.deleted_at.is_(None),
        )
    )
    enrolments = result.scalars().all()
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "organization_id": user.organization_id,
        "global_role": user.global_role.value,
        "enrolments": [
            {"id": e.id, "cohort_id": e.cohort_id, "role": e.role.value, "status": e.status.value}
            for e in enrolments
        ],
    }
