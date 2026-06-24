"""Tenant isolation matrix (ADR-002 invariant: org data must never cross org boundaries).

For each org-scoped endpoint, verify:
  - Learner from Org A cannot read Org B's data
  - Submission from Org A cannot be accessed by Org B's learner
  - Facilitator from Org A cannot override Org B's progress
"""
import json

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import (
    Cohort, CohortStatus, Enrolment, EnrolmentRole,
    Organization, User, UserAuthProvider, UserGlobalRole
)
from src.db.models.curriculum import Curriculum, CurriculumEdition, CurriculumStatus
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.models.submission import Submission, SubmissionStatus
from src.db.uuidv7 import uuid7_str
from src.lib.jwt import hash_password
from tests.conftest import make_auth_header


@pytest.fixture
async def org_b(db: AsyncSession) -> Organization:
    o = Organization(
        id=uuid7_str(),
        name="Org B",
        slug="org-b-" + uuid7_str()[:6],
        edition="co_worker",
        region="ap-southeast-1",
    )
    db.add(o)
    await db.flush()
    return o


@pytest.fixture
async def learner_b(db: AsyncSession, org_b: Organization) -> User:
    u = User(
        id=uuid7_str(),
        organization_id=org_b.id,
        email="learner-b@orgb.example",
        display_name="Learner B",
        auth_provider=UserAuthProvider.local,
        password_hash=hash_password("password123"),
        global_role=UserGlobalRole.learner,
    )
    db.add(u)
    await db.flush()
    return u


@pytest.fixture
async def cohort_b(db: AsyncSession, org_b: Organization, curriculum) -> Cohort:
    c = Cohort(
        id=uuid7_str(),
        organization_id=org_b.id,
        curriculum_id=curriculum.id,
        name="Cohort B",
        status=CohortStatus.running,
    )
    db.add(c)
    await db.flush()
    return c


@pytest.fixture
async def enrolment_b(db: AsyncSession, cohort_b: Cohort, learner_b: User) -> Enrolment:
    e = Enrolment(
        id=uuid7_str(),
        cohort_id=cohort_b.id,
        user_id=learner_b.id,
        role=EnrolmentRole.learner,
    )
    db.add(e)
    await db.flush()
    return e


@pytest.mark.asyncio
async def test_learner_cannot_access_other_org_cohort_modules(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    cohort_b: Cohort,
):
    """Learner from Org A gets 403/404 when requesting Org B's cohort modules."""
    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/cohorts/{cohort_b.id}/modules", headers=headers)
    assert resp.status_code in (403, 404)


@pytest.mark.asyncio
async def test_learner_b_cannot_access_org_a_submission(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    learner_b: User,
    enrolment,
    exercise,
    progress,
):
    """Learner B should not be able to read Learner A's submission."""
    from datetime import datetime, timezone

    sub = Submission(
        id=uuid7_str(),
        exercise_progress_id=progress.id,
        enrolment_id=enrolment.id,
        exercise_id=exercise.id,
        attempt_number=1,
        payload=json.dumps({"schema_version": "1.0"}),
        status=SubmissionStatus.queued,
        idempotency_key=uuid7_str(),
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(sub)
    await db.flush()

    headers_b = make_auth_header(learner_b)
    resp = await client.get(f"/v1/submissions/{sub.id}", headers=headers_b)
    assert resp.status_code in (403, 404)


@pytest.mark.xfail(
    strict=True,
    reason="BUG-003: apply_facilitator_override does not verify org ownership — cross-org override succeeds with 200",
)
@pytest.mark.asyncio
async def test_facilitator_cannot_override_other_org_progress(
    client: AsyncClient,
    db: AsyncSession,
    facilitator: User,
    enrolment_b: Enrolment,
    exercise,
):
    """Facilitator from Org A cannot override Org B learner's progress.

    BUG-003: progress/service.apply_facilitator_override only checks role=facilitator but
    does NOT verify the facilitator's org_id matches the progress record's org.
    Fix: load enrolment → cohort → organization_id and compare against user.organization_id.
    """
    progress_b = ExerciseProgress(
        id=uuid7_str(),
        enrolment_id=enrolment_b.id,
        exercise_id=exercise.id,
        phase=ExercisePhase.exploring,
    )
    db.add(progress_b)
    await db.flush()

    headers = make_auth_header(facilitator)
    resp = await client.post(
        f"/v1/facilitator/progress/{progress_b.id}/override",
        json={"action": "unlock_consolidation", "reason": "test"},
        headers=headers,
    )
    assert resp.status_code in (403, 404)


@pytest.mark.asyncio
async def test_learner_cannot_see_other_org_exercise_progress(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment_b,
    exercise,
):
    """Learner A querying progress for an exercise enrolled under Org B → not found."""
    progress_b = ExerciseProgress(
        id=uuid7_str(),
        enrolment_id=enrolment_b.id,
        exercise_id=exercise.id,
        phase=ExercisePhase.exploring,
    )
    db.add(progress_b)
    await db.flush()

    headers = make_auth_header(learner)
    resp = await client.get(f"/v1/exercises/{exercise.id}/progress", headers=headers)
    # Learner A has no enrolment for this exercise → 404 or 403
    assert resp.status_code in (403, 404)
