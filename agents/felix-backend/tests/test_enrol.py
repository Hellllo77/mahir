"""Student join endpoint tests — POST /v1/cohorts/{id}/enrol?token=X"""
from datetime import datetime, timedelta, timezone

import pytest
from httpx import AsyncClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.db.models.auth import CohortStatus, Cohort, Enrolment, EnrolmentRole, Organization, User
from src.db.uuidv7 import uuid7_str
from tests.conftest import make_user


def make_invite_token(cohort_id: str, org_id: str, expires_delta: timedelta = timedelta(days=7)) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    return jwt.encode(
        {"cohort_id": cohort_id, "org_id": org_id, "type": "invite", "exp": expire},
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


@pytest.fixture
async def active_cohort(db: AsyncSession, org: Organization) -> Cohort:
    c = Cohort(
        id=uuid7_str(),
        organization_id=org.id,
        name="Active Cohort",
        status=CohortStatus.active,
    )
    db.add(c)
    await db.flush()
    return c


@pytest.mark.asyncio
async def test_enrol_new_user_happy_path(
    client: AsyncClient, db: AsyncSession, active_cohort: Cohort, org: Organization
):
    token = make_invite_token(active_cohort.id, org.id)
    resp = await client.post(
        f"/v1/cohorts/{active_cohort.id}/enrol",
        params={"token": token},
        json={
            "email": "newstudent@example.com",
            "display_name": "New Student",
            "password": "Secur3Pass!",
        },
    )
    assert resp.status_code == 201, resp.json()
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "expires_in" in data
    assert "enrolment_id" in data


@pytest.mark.asyncio
async def test_enrol_existing_user_creates_enrolment(
    client: AsyncClient, db: AsyncSession, active_cohort: Cohort, org: Organization, learner: User
):
    """Existing user with no prior enrolment gets enrolled without providing password."""
    token = make_invite_token(active_cohort.id, org.id)
    resp = await client.post(
        f"/v1/cohorts/{active_cohort.id}/enrol",
        params={"token": token},
        json={"email": learner.email},
    )
    assert resp.status_code == 201, resp.json()
    data = resp.json()
    assert "access_token" in data
    assert "enrolment_id" in data


@pytest.mark.asyncio
async def test_enrol_already_enrolled_returns_409(
    client: AsyncClient, db: AsyncSession, active_cohort: Cohort, org: Organization, learner: User
):
    """Duplicate enrolment must return 409."""
    # First enrolment
    existing = Enrolment(
        id=uuid7_str(),
        cohort_id=active_cohort.id,
        user_id=learner.id,
        role=EnrolmentRole.learner,
    )
    db.add(existing)
    await db.flush()

    token = make_invite_token(active_cohort.id, org.id)
    resp = await client.post(
        f"/v1/cohorts/{active_cohort.id}/enrol",
        params={"token": token},
        json={"email": learner.email},
    )
    assert resp.status_code == 409, resp.json()


@pytest.mark.asyncio
async def test_enrol_expired_token_returns_401(
    client: AsyncClient, db: AsyncSession, active_cohort: Cohort, org: Organization
):
    token = make_invite_token(active_cohort.id, org.id, expires_delta=timedelta(seconds=-1))
    resp = await client.post(
        f"/v1/cohorts/{active_cohort.id}/enrol",
        params={"token": token},
        json={"email": "late@example.com", "display_name": "Late", "password": "Pass1234"},
    )
    assert resp.status_code == 401, resp.json()


@pytest.mark.asyncio
async def test_enrol_cohort_not_active_returns_403(
    client: AsyncClient, db: AsyncSession, org: Organization
):
    """Draft cohort rejects enrolments."""
    draft_cohort = Cohort(
        id=uuid7_str(),
        organization_id=org.id,
        name="Draft Cohort",
        status=CohortStatus.draft,
    )
    db.add(draft_cohort)
    await db.flush()

    token = make_invite_token(draft_cohort.id, org.id)
    resp = await client.post(
        f"/v1/cohorts/{draft_cohort.id}/enrol",
        params={"token": token},
        json={"email": "student@example.com", "display_name": "Student", "password": "Pass1234"},
    )
    assert resp.status_code == 403, resp.json()


@pytest.mark.asyncio
async def test_enrol_new_user_missing_password_returns_400(
    client: AsyncClient, db: AsyncSession, active_cohort: Cohort, org: Organization
):
    token = make_invite_token(active_cohort.id, org.id)
    resp = await client.post(
        f"/v1/cohorts/{active_cohort.id}/enrol",
        params={"token": token},
        json={"email": "nopass@example.com", "display_name": "No Pass"},
    )
    assert resp.status_code == 400, resp.json()
