"""Curriculum module tests — module listing, exercise get, PF gate on consolidation."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Enrolment, EnrolmentRole, User
from src.db.models.curriculum import ConsolidationContent, Exercise, Module
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.uuidv7 import uuid7_str
from tests.conftest import make_auth_header


@pytest.mark.asyncio
async def test_list_modules_requires_auth(client: AsyncClient, cohort):
    resp = await client.get(f"/v1/cohorts/{cohort.id}/modules")
    assert resp.status_code == 401  # HTTPBearer returns 401 in FastAPI >=0.115


@pytest.mark.asyncio
async def test_list_modules(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    cohort,
    enrolment: Enrolment,
    module: Module,
):
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/cohorts/{cohort.id}/modules", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert any(m["id"] == module.id for m in data)


@pytest.mark.asyncio
async def test_get_exercise(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
):
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/exercises/{exercise.id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == exercise.id
    # consolidation must NOT be in the exercise response
    assert "body_markdown" not in data
    assert "reference_build" not in data


@pytest.mark.asyncio
async def test_consolidation_locked_when_exploring(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    # progress fixture starts in exploring phase
    assert progress.phase == ExercisePhase.exploring

    cc = ConsolidationContent(
        id=uuid7_str(),
        exercise_id=exercise.id,
        body_markdown="# Reference solution",
    )
    db.add(cc)
    await db.flush()

    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/exercises/{exercise.id}/consolidation", headers=headers)
    assert resp.status_code == 409
    assert resp.json()["detail"]["type"] == "phase_locked"


@pytest.mark.asyncio
async def test_consolidation_unlocked_after_gate(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    # Manually advance phase to consolidation_unlocked
    progress.phase = ExercisePhase.consolidation_unlocked
    await db.flush()

    cc = ConsolidationContent(
        id=uuid7_str(),
        exercise_id=exercise.id,
        body_markdown="# Reference solution\n\nHere's how to build it.",
    )
    db.add(cc)
    await db.flush()

    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/exercises/{exercise.id}/consolidation", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "body_markdown" in data


@pytest.mark.asyncio
async def test_consolidation_gate_not_bypassed_without_enrolment(
    client: AsyncClient,
    db: AsyncSession,
    org,
    curriculum,
    module: Module,
    exercise: Exercise,
):
    """A user with no enrolment cannot access consolidation."""
    from src.db.models.auth import UserAuthProvider
    from src.lib.jwt import hash_password

    stranger = User(
        id=uuid7_str(),
        organization_id=org.id,
        email="stranger@test.example",
        display_name="Stranger",
        auth_provider=UserAuthProvider.local,
        password_hash=hash_password("password123"),
    )
    db.add(stranger)
    await db.flush()

    headers = make_auth_header(stranger)
    resp = await client.get(f"/v1/exercises/{exercise.id}/consolidation", headers=headers)
    # Must be forbidden (no enrolment), not 200
    assert resp.status_code in (403, 404)
