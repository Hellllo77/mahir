from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Cohort, Enrolment, User, UserGlobalRole
from src.lib.exceptions import forbidden

_ALLOWED = {UserGlobalRole.org_admin, UserGlobalRole.super_admin, UserGlobalRole.facilitator}


async def list_cohorts(db: AsyncSession, user: User) -> list[dict]:
    if user.global_role not in _ALLOWED:
        raise forbidden("org_admin, super_admin, or facilitator role required.")

    learner_count_sq = (
        select(func.count(Enrolment.id))
        .where(
            Enrolment.cohort_id == Cohort.id,
            Enrolment.status == "active",
            Enrolment.deleted_at.is_(None),
        )
        .correlate(Cohort)
        .scalar_subquery()
    )

    result = await db.execute(
        select(Cohort, learner_count_sq.label("learner_count"))
        .where(
            Cohort.organization_id == user.organization_id,
            Cohort.deleted_at.is_(None),
        )
        .order_by(Cohort.created_at.desc())
    )

    return [
        {
            "id": cohort.id,
            "name": cohort.name,
            "status": cohort.status if isinstance(cohort.status, str) else cohort.status.value,
            "learner_count": count,
        }
        for cohort, count in result.all()
    ]
