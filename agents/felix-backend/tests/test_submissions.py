"""Submission module tests — submit, idempotency, status, tenant access."""
import json
from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Enrolment, User
from src.db.models.curriculum import Exercise
from src.db.models.progress import ExerciseProgress
from src.db.uuidv7 import uuid7_str
from tests.conftest import make_auth_header

_MOCK_ENQUEUE = patch("src.submissions.service.enqueue_evaluation")

_VALID_PAYLOAD = {
    "schema_version": "1.0",
    "model": "claude-haiku-4-5",
    "tools": [{"name": "classify", "description": "Classify text sentiment"}],
}


@pytest.mark.asyncio
async def test_submit_creates_submission(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    headers = {**make_auth_header(learner), "Idempotency-Key": str(uuid7_str())}
    with _MOCK_ENQUEUE:
        resp = await client.post(
            f"/v1/exercises/{exercise.id}/submissions",
            json={"payload": _VALID_PAYLOAD, "artifact_refs": None},
            headers=headers,
        )
    assert resp.status_code == 202
    data = resp.json()
    assert data["exercise_id"] == exercise.id
    assert data["status"] == "queued"


@pytest.mark.asyncio
async def test_submit_idempotency(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    idem_key = str(uuid7_str())
    headers = {**make_auth_header(learner), "Idempotency-Key": idem_key}
    body = {"payload": _VALID_PAYLOAD, "artifact_refs": None}

    with _MOCK_ENQUEUE:
        resp1 = await client.post(f"/v1/exercises/{exercise.id}/submissions", json=body, headers=headers)
        resp2 = await client.post(f"/v1/exercises/{exercise.id}/submissions", json=body, headers=headers)

    assert resp1.status_code == 202
    assert resp2.status_code == 202
    assert resp1.json()["id"] == resp2.json()["id"]


@pytest.mark.asyncio
async def test_submit_requires_idempotency_key(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    headers = make_auth_header(learner)
    with _MOCK_ENQUEUE:
        resp = await client.post(
            f"/v1/exercises/{exercise.id}/submissions",
            json={"payload": _VALID_PAYLOAD, "artifact_refs": None},
            headers=headers,
        )
    assert resp.status_code == 422  # missing required header


@pytest.mark.asyncio
async def test_list_submissions(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    idem_key = str(uuid7_str())
    headers = {**make_auth_header(learner), "Idempotency-Key": idem_key}
    with _MOCK_ENQUEUE:
        await client.post(
            f"/v1/exercises/{exercise.id}/submissions",
            json={"payload": _VALID_PAYLOAD, "artifact_refs": None},
            headers=headers,
        )

    list_resp = await client.get(
        f"/v1/exercises/{exercise.id}/submissions",
        headers=make_auth_header(learner),
    )
    assert list_resp.status_code == 200
    items = list_resp.json()
    assert len(items) >= 1
    assert items[0]["exercise_id"] == exercise.id


@pytest.mark.asyncio
async def test_get_submission_detail(
    client: AsyncClient,
    db: AsyncSession,
    learner: User,
    enrolment: Enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    idem_key = str(uuid7_str())
    headers = {**make_auth_header(learner), "Idempotency-Key": idem_key}
    with _MOCK_ENQUEUE:
        create_resp = await client.post(
            f"/v1/exercises/{exercise.id}/submissions",
            json={"payload": _VALID_PAYLOAD, "artifact_refs": None},
            headers=headers,
        )
    sub_id = create_resp.json()["id"]

    detail_resp = await client.get(
        f"/v1/submissions/{sub_id}",
        headers=make_auth_header(learner),
    )
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == sub_id
