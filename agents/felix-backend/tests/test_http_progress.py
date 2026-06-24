"""HTTP-layer integration tests — progress + facilitator endpoints.

Covers routes not tested elsewhere:
  GET  /me/progress?enrolment_id=<id>           (and documents BUG-001 camelCase variant)
  GET  /exercises/{id}/progress
  GET  /facilitator/cohorts/{id}/learners
  POST /facilitator/progress/{id}/override
"""
import json

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Cohort, CohortStatus, Enrolment, EnrolmentRole, User, UserGlobalRole
from src.db.models.curriculum import Exercise
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.uuidv7 import uuid7_str
from tests.conftest import make_auth_header, make_user


# ── GET /me/progress ─────────────────────────────────────────────────────────


@pytest.mark.xfail(
    strict=True,
    reason="BUG-002: progress/service.py:27 passes `db` instead of `exercise` to _progress_to_dict — causes 500",
)
@pytest.mark.asyncio
async def test_get_my_progress_returns_list(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    """GET /me/progress should return a list of progress dicts with gate info.

    BUG-002: service.get_my_progress (line 27) calls _progress_to_dict(p, db) passing
    the AsyncSession as the second arg instead of the Exercise. Causes AttributeError
    (500) on any call. Fix: either pass exercise=None (drops gate block) or fetch
    and pass the Exercise objects.
    """
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/me/progress?enrolment_id={enrolment.id}", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(p["exercise_id"] == exercise.id for p in data)


@pytest.mark.asyncio
async def test_get_my_progress_unauthenticated_returns_401(client: AsyncClient, enrolment: Enrolment):
    resp = await client.get(f"/v1/me/progress?enrolment_id={enrolment.id}")
    assert resp.status_code == 401  # HTTPBearer returns 401 in FastAPI >=0.115


@pytest.mark.asyncio
async def test_get_my_progress_wrong_enrolment_returns_404(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
):
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/me/progress?enrolment_id={uuid7_str()}", headers=headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_my_progress_camelcase_param_currently_returns_422(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    progress: ExerciseProgress,
):
    """BUG-001 — documents current broken behaviour.

    mahir-api.yaml declares query param as 'enrolmentId' (camelCase).
    The frontend sends ?enrolmentId=... (correct per contract).
    The FastAPI router uses enrolment_id (snake_case) without alias → 422.
    Fix: add alias='enrolmentId' to Query(...) in progress/router.py.
    Once fixed, this test must be updated to assert 200 and the xfail below removed.
    """
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/me/progress?enrolmentId={enrolment.id}", headers=headers)
    assert resp.status_code == 422  # BLOCKING bug — frontend cannot call this endpoint


@pytest.mark.xfail(
    strict=True,
    reason="BUG-001: progress/router.py needs alias='enrolmentId' on Query — remove xfail once fixed",
)
@pytest.mark.asyncio
async def test_get_my_progress_camelcase_param_desired_behaviour(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    progress: ExerciseProgress,
):
    """Target state after BUG-001 fix: camelCase param must return 200."""
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/me/progress?enrolmentId={enrolment.id}", headers=headers)
    assert resp.status_code == 200


# ── GET /exercises/{id}/progress ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_exercise_progress_returns_phase(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/exercises/{exercise.id}/progress", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["exercise_id"] == exercise.id
    assert data["phase"] == "exploring"
    assert "gate" in data


@pytest.mark.asyncio
async def test_get_exercise_progress_unauthenticated_returns_401(
    client: AsyncClient, exercise: Exercise
):
    resp = await client.get(f"/v1/exercises/{exercise.id}/progress")
    assert resp.status_code == 401  # HTTPBearer returns 401 in FastAPI >=0.115


@pytest.mark.asyncio
async def test_get_exercise_progress_no_enrolment_returns_403_or_404(
    client: AsyncClient,
    db: AsyncSession,
    org,
    curriculum,
    exercise: Exercise,
):
    """User with no enrolment for the exercise's curriculum is rejected."""
    stranger = make_user(org)
    db.add(stranger)
    await db.flush()

    headers = make_auth_header(stranger)
    resp = await client.get(f"/v1/exercises/{exercise.id}/progress", headers=headers)
    assert resp.status_code in (403, 404)


@pytest.mark.asyncio
async def test_get_exercise_progress_nonexistent_exercise_returns_404(
    client: AsyncClient,
    learner: User,
):
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/exercises/{uuid7_str()}/progress", headers=headers)
    assert resp.status_code == 404


# ── GET /facilitator/cohorts/{id}/learners ───────────────────────────────────


@pytest.mark.asyncio
async def test_get_cohort_learners_facilitator_succeeds(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    cohort: Cohort,
    enrolment: Enrolment,
    learner: User,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    headers = make_auth_header(facilitator)
    resp = await client.get(f"/v1/facilitator/cohorts/{cohort.id}/learners", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    user_ids = [s["user_id"] for s in data]
    assert learner.id in user_ids


@pytest.mark.asyncio
async def test_get_cohort_learners_learner_role_denied(
    client: AsyncClient,
    learner: User,
    cohort: Cohort,
):
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/facilitator/cohorts/{cohort.id}/learners", headers=headers)
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_get_cohort_learners_other_org_denied(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    org2,
    curriculum,
):
    """Facilitator from Org A cannot list learners of Org B's cohort."""
    cohort_b = Cohort(
        id=uuid7_str(),
        organization_id=org2.id,
        curriculum_id=curriculum.id,
        name="Cohort B",
        status=CohortStatus.running,
    )
    db.add(cohort_b)
    await db.flush()

    headers = make_auth_header(facilitator)
    resp = await client.get(f"/v1/facilitator/cohorts/{cohort_b.id}/learners", headers=headers)
    assert resp.status_code in (403, 404)


@pytest.mark.asyncio
async def test_get_cohort_learners_unauthenticated_returns_401(
    client: AsyncClient, cohort: Cohort
):
    resp = await client.get(f"/v1/facilitator/cohorts/{cohort.id}/learners")
    assert resp.status_code == 401  # HTTPBearer returns 401 in FastAPI >=0.115


# ── POST /facilitator/progress/{id}/override ─────────────────────────────────


@pytest.mark.asyncio
async def test_override_unlock_consolidation(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    progress: ExerciseProgress,
):
    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress.id}/override",
        json={"action": "unlock_consolidation", "reason": "Pilot exception — learner has verbal approval"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["phase"] == "consolidation_unlocked"
    assert data["explored"] is False  # facilitator bypass sets explored=False per ADR-004


@pytest.mark.asyncio
async def test_override_mark_completed(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    progress: ExerciseProgress,
):
    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress.id}/override",
        json={"action": "mark_completed", "reason": "Assessment passed offline"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["phase"] == "completed"


@pytest.mark.asyncio
async def test_override_reset_exploring(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    progress: ExerciseProgress,
):
    progress.phase = ExercisePhase.consolidation_unlocked
    await db.flush()

    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress.id}/override",
        json={"action": "reset_exploring", "reason": "Learner wants to redo from scratch"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["phase"] == "exploring"


@pytest.mark.asyncio
async def test_override_unknown_action_returns_400(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    progress: ExerciseProgress,
):
    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress.id}/override",
        json={"action": "delete_everything", "reason": "test"},
        headers=headers,
    )
    assert resp.status_code in (400, 422)


@pytest.mark.asyncio
async def test_override_learner_role_denied(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    progress: ExerciseProgress,
):
    headers = make_auth_header(learner)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress.id}/override",
        json={"action": "unlock_consolidation", "reason": "self-unlock attempt"},
        headers=headers,
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_override_nonexistent_progress_returns_404(
    client: AsyncClient,
    facilitator: User,
):
    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{uuid7_str()}/override",
        json={"action": "unlock_consolidation", "reason": "does not exist"},
        headers=headers,
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_override_missing_reason_returns_422(
    client: AsyncClient,
    facilitator: User,
    progress: ExerciseProgress,
):
    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress.id}/override",
        json={"action": "unlock_consolidation"},  # missing required 'reason'
        headers=headers,
    )
    assert resp.status_code == 422
