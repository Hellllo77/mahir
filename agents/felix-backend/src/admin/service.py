"""Admin settings service — org-scoped config (Resend key, OpenRouter key + model)."""
from typing import Optional

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
    s = result.scalar_one_or_none()
    return {
        "resend_api_key": mask_api_key(s.resend_api_key if s else None),
        "openrouter_api_key": mask_api_key(s.openrouter_api_key if s else None),
        "preferred_model": s.preferred_model if s else None,
    }


async def update_settings(
    db: AsyncSession,
    user: User,
    resend_api_key: Optional[str] = None,
    openrouter_api_key: Optional[str] = None,
    preferred_model: Optional[str] = None,
) -> dict:
    if user.global_role not in _ADMIN_ROLES:
        raise forbidden("org_admin or super_admin role required.")

    result = await db.execute(
        select(OrganisationSettings).where(
            OrganisationSettings.org_id == user.organization_id,
        )
    )
    s = result.scalar_one_or_none()

    if s is None:
        s = OrganisationSettings(
            id=uuid7_str(),
            org_id=user.organization_id,
        )
        db.add(s)

    if resend_api_key is not None:
        s.resend_api_key = resend_api_key
    if openrouter_api_key is not None:
        s.openrouter_api_key = openrouter_api_key
    if preferred_model is not None:
        s.preferred_model = preferred_model
    s.updated_by = user.id
    await db.flush()

    return {
        "resend_api_key": mask_api_key(s.resend_api_key),
        "openrouter_api_key": mask_api_key(s.openrouter_api_key),
        "preferred_model": s.preferred_model,
    }
