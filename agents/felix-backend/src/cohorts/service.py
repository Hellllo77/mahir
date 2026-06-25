from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cohorts.schemas import CohortCreate
from src.db.models.auth import Cohort, CohortStatus, Enrolment, User, UserGlobalRole
from src.db.uuidv7 import uuid7_str
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


async def create_cohort(db: AsyncSession, user: User, payload: CohortCreate) -> dict:
    if user.global_role not in _ALLOWED:
        raise forbidden("org_admin, super_admin, or facilitator role required.")

    cohort = Cohort(
        id=uuid7_str(),
        organization_id=user.organization_id,
        name=payload.name,
        description=payload.description,
        starts_on=payload.start_date.isoformat() if payload.start_date else None,
        status=CohortStatus.draft,
    )
    db.add(cohort)
    await db.commit()
    await db.refresh(cohort)

    return {
        "id": cohort.id,
        "name": cohort.name,
        "description": cohort.description,
        "status": cohort.status if isinstance(cohort.status, str) else cohort.status.value,
        "starts_on": cohort.starts_on,
    }
