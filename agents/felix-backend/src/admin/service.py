"""Admin settings service — org-scoped config (Resend key, OpenRouter key + model)."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.schemas import SettingsUpdate
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


async def update_settings(db: AsyncSession, user: User, body: SettingsUpdate) -> dict:
    """Partial update — only fields present in the request body are written.

    Explicit null clears the field; omitting a field leaves it unchanged.
    Uses model_fields_set to distinguish omitted from explicitly-null.
    """
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

    provided = body.model_fields_set
    if "resend_api_key" in provided:
        s.resend_api_key = body.resend_api_key
    if "openrouter_api_key" in provided:
        s.openrouter_api_key = body.openrouter_api_key
    if "preferred_model" in provided:
        s.preferred_model = body.preferred_model
    s.updated_by = user.id
    await db.flush()

    return {
        "resend_api_key": mask_api_key(s.resend_api_key),
        "openrouter_api_key": mask_api_key(s.openrouter_api_key),
        "preferred_model": s.preferred_model,
    }
