"""Admin settings service — org-scoped config (Resend API key etc)."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.admin import OrganisationSettings
from src.db.models.auth import User, UserGlobalRole
from src.db.uuidv7 import uuid7_str
from src.lib.email import mask_api_key
from src.lib.exceptions import forbidden

_ADMIN_ROLES = {UserGlobalRole.org_admin, UserGlobalRole.super_admin}


async def get_settings(db: AsyncSession, user: User) -> dict:
    if user.global_role not in _ADMIN_ROLES:
        raise forbidden("org_admin or super_admin role required.")

    result = await db.execute(
        select(OrganisationSettings).where(
            OrganisationSettings.org_id == user.organization_id,
                    )
    )
    settings = result.scalar_one_or_none()
    return {"resend_api_key": mask_api_key(settings.resend_api_key if settings else None)}


async def update_settings(db: AsyncSession, user: User, resend_api_key: str) -> dict:
    if user.global_role not in _ADMIN_ROLES:
        raise forbidden("org_admin or super_admin role required.")

    result = await db.execute(
        select(OrganisationSettings).where(
            OrganisationSettings.org_id == user.organization_id,
                    )
    )
    settings = result.scalar_one_or_none()

    if settings is None:
        settings = OrganisationSettings(
            id=uuid7_str(),
            org_id=user.organization_id,
        )
        db.add(settings)

    settings.resend_api_key = resend_api_key
    settings.updated_by = user.id
    await db.flush()

    return {"resend_api_key": mask_api_key(settings.resend_api_key)}
