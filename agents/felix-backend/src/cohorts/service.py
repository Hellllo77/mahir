from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.cohorts.schemas import CohortCreate, EnrolRequest
from src.config import settings
from src.db.models.auth import (
    Cohort, CohortStatus, Enrolment, EnrolmentRole, EnrolmentStatus,
    User, UserAuthProvider, UserGlobalRole, UserStatus,
)
from src.db.models.curriculum import Curriculum, CurriculumStatus
from src.db.uuidv7 import uuid7_str
from src.lib.exceptions import bad_request, conflict, forbidden, not_found, unauthorized
from src.lib.jwt import create_access_token, hash_password

_ALLOWED = {UserGlobalRole.org_admin, UserGlobalRole.super_admin, UserGlobalRole.facilitator}

# Statuses a facilitator can set via PATCH /cohorts/:id
_ALLOWED_STATUS_TRANSITIONS: dict[str, set[str]] = {
    CohortStatus.draft.value:    {CohortStatus.active.value},
    CohortStatus.active.value:   {CohortStatus.draft.value, CohortStatus.completed.value},
    CohortStatus.running.value:  {CohortStatus.active.value, CohortStatus.completed.value},
    CohortStatus.completed.value: {CohortStatus.archived.value},
    CohortStatus.archived.value:  set(),
}


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
            "status": cohort.status.value if isinstance(cohort.status, CohortStatus) else str(cohort.status),
            "learner_count": count,
        }
        for cohort, count in result.all()
    ]


async def create_cohort(db: AsyncSession, user: User, payload: CohortCreate) -> dict:
    if user.global_role not in _ALLOWED:
        raise forbidden("org_admin, super_admin, or facilitator role required.")

    curriculum_result = await db.execute(
        select(Curriculum).where(
            Curriculum.status == CurriculumStatus.published,
            Curriculum.deleted_at.is_(None),
        ).limit(1)
    )
    curriculum = curriculum_result.scalar_one_or_none()

    cohort = Cohort(
        id=uuid7_str(),
        organization_id=user.organization_id,
        name=payload.name,
        description=payload.description,
        starts_on=payload.start_date.isoformat() if payload.start_date else None,
        status=CohortStatus.draft,
        curriculum_id=curriculum.id if curriculum else None,
    )
    db.add(cohort)
    await db.commit()
    await db.refresh(cohort)

    return {
        "id": cohort.id,
        "name": cohort.name,
        "description": cohort.description,
        "status": cohort.status.value if isinstance(cohort.status, CohortStatus) else str(cohort.status),
        "starts_on": cohort.starts_on,
        "enrollment_count": 0,
    }


async def get_cohort(db: AsyncSession, user: User, cohort_id: str) -> dict:
    if user.global_role not in _ALLOWED:
        raise forbidden("org_admin, super_admin, or facilitator role required.")

    result = await db.execute(
        select(Cohort).where(
            Cohort.id == cohort_id,
            Cohort.organization_id == user.organization_id,
            Cohort.deleted_at.is_(None),
        )
    )
    cohort = result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort not found.")

    learner_count_sq = (
        select(func.count(Enrolment.id))
        .where(
            Enrolment.cohort_id == cohort.id,
            Enrolment.status == "active",
            Enrolment.deleted_at.is_(None),
        )
        .scalar_subquery()
    )
    count_result = await db.execute(select(learner_count_sq))
    enrollment_count = count_result.scalar() or 0

    return {
        "id": cohort.id,
        "name": cohort.name,
        "description": cohort.description,
        "status": cohort.status.value if isinstance(cohort.status, CohortStatus) else str(cohort.status),
        "starts_on": cohort.starts_on,
        "enrollment_count": enrollment_count,
    }


async def update_cohort(
    db: AsyncSession,
    user: User,
    cohort_id: str,
    status: str | None,
    name: str | None,
    description: str | None,
) -> dict:
    if user.global_role not in _ALLOWED:
        raise forbidden("org_admin, super_admin, or facilitator role required.")

    result = await db.execute(
        select(Cohort).where(
            Cohort.id == cohort_id,
            Cohort.organization_id == user.organization_id,
            Cohort.deleted_at.is_(None),
        )
    )
    cohort = result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort not found.")

    # Query enrollment count before modifying session state
    count_result = await db.execute(
        select(func.count(Enrolment.id)).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.status == "active",
            Enrolment.deleted_at.is_(None),
        )
    )
    enrollment_count = count_result.scalar() or 0

    # Use .value to get plain string — CohortStatus is str+Enum so isinstance(x, str) is True
    # but str(x) / f"{x}" returns "CohortStatus.X" not "X"
    new_status = cohort.status.value if isinstance(cohort.status, CohortStatus) else str(cohort.status)
    if status is not None:
        current = new_status
        allowed_next = _ALLOWED_STATUS_TRANSITIONS.get(current, set())
        if status not in allowed_next:
            raise forbidden(f"Cannot transition cohort from '{current}' to '{status}'.")
        # Assign enum member (not plain string) so asyncpg uses the enum OID,
        # which works with both native PG ENUM columns and TEXT columns.
        cohort.status = CohortStatus(status)
        new_status = status

    if name is not None:
        cohort.name = name
    if description is not None:
        cohort.description = description

    # Flush sends the UPDATE SQL in the current transaction; get_db() commits once at route exit.
    # Avoids the double-commit pattern (explicit commit + get_db commit) that creates a second
    # implicit transaction via db.refresh and can cause asyncpg errors on pooled connections.
    await db.flush()

    return {
        "id": cohort.id,
        "name": cohort.name,
        "description": cohort.description,
        "status": new_status,
        "starts_on": cohort.starts_on,
        "enrollment_count": enrollment_count,
    }


async def enrol_student(
    db: AsyncSession, cohort_id: str, token: str, payload: EnrolRequest
) -> dict:
    # Validate invite token
    try:
        claims = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise unauthorized("Invalid or expired invite token.")
    if claims.get("type") != "invite":
        raise unauthorized("Invalid invite token.")
    if claims.get("cohort_id") != cohort_id:
        raise unauthorized("Token does not match this cohort.")
    org_id: str = claims.get("org_id", "")

    # Cohort must exist and be active
    cohort_result = await db.execute(
        select(Cohort).where(Cohort.id == cohort_id, Cohort.deleted_at.is_(None))
    )
    cohort = cohort_result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort")
    cohort_status = cohort.status.value if isinstance(cohort.status, CohortStatus) else str(cohort.status)
    if cohort_status != CohortStatus.active.value:
        raise forbidden("Cohort is not accepting enrolments.")

    email = (payload.email or "").strip().lower()
    if not email:
        raise bad_request("email is required.")

    # Look up existing user (same org + email)
    user_result = await db.execute(
        select(User).where(
            User.email == email,
            User.organization_id == org_id,
            User.deleted_at.is_(None),
        )
    )
    user = user_result.scalar_one_or_none()

    if user is None:
        # New user — require name + password
        if not payload.display_name:
            raise bad_request("display_name is required for new users.")
        if not payload.password:
            raise bad_request("password is required for new users.")

        user = User(
            id=uuid7_str(),
            organization_id=org_id,
            email=email,
            display_name=payload.display_name.strip(),
            auth_provider=UserAuthProvider.local,
            password_hash=hash_password(payload.password),
            global_role=UserGlobalRole.learner,
            status=UserStatus.active,
        )
        db.add(user)
        await db.flush()

    # Check not already enrolled
    existing_result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.user_id == user.id,
            Enrolment.deleted_at.is_(None),
        )
    )
    existing_enrolment = existing_result.scalar_one_or_none()
    if existing_enrolment is not None:
        raise conflict("Already enrolled in this cohort.", type_="already_enrolled")

    enrolment = Enrolment(
        id=uuid7_str(),
        cohort_id=cohort_id,
        user_id=user.id,
        role=EnrolmentRole.learner,
        status=EnrolmentStatus.active,
    )
    db.add(enrolment)
    await db.flush()

    access_token, expires_in = create_access_token(user.id, user.organization_id, user.global_role.value)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "enrolment_id": enrolment.id,
    }


async def get_invite_link(db: AsyncSession, user: User, cohort_id: str) -> dict:
    if user.global_role not in _ALLOWED:
        raise forbidden("org_admin, super_admin, or facilitator role required.")

    result = await db.execute(
        select(Cohort).where(
            Cohort.id == cohort_id,
            Cohort.organization_id == user.organization_id,
            Cohort.deleted_at.is_(None),
        )
    )
    cohort = result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort not found.")

    expire = datetime.now(timezone.utc) + timedelta(days=7)
    token = jwt.encode(
        {"cohort_id": cohort_id, "org_id": str(user.organization_id), "type": "invite", "exp": expire},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    frontend_url = settings.frontend_url.rstrip("/")
    url = f"{frontend_url}/cohorts/{cohort_id}/join?token={token}"
    return {"url": url}
