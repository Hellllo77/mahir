"""Tenant isolation helpers — ensure queries never cross org boundaries (ADR-002)."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Cohort, Enrolment, User
from src.lib.exceptions import forbidden, not_found


async def assert_cohort_access(db: AsyncSession, cohort_id: str, user: User) -> Cohort:
    """Return the cohort only if it belongs to the user's org and the user is enrolled (or is admin)."""
    result = await db.execute(
        select(Cohort).where(Cohort.id == cohort_id, Cohort.deleted_at.is_(None))
    )
    cohort = result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort")
    if cohort.organization_id != user.organization_id:
        raise forbidden()
    return cohort


async def get_enrolment_for_user(db: AsyncSession, cohort_id: str, user_id: str) -> Enrolment | None:
    result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.user_id == user_id,
            Enrolment.deleted_at.is_(None),
        )
    )
    return result.scalar_one_or_none()


async def assert_enrolment(db: AsyncSession, cohort_id: str, user: User) -> Enrolment:
    enrolment = await get_enrolment_for_user(db, cohort_id, user.id)
    if enrolment is None:
        raise forbidden("Not enrolled in this cohort.")
    return enrolment
