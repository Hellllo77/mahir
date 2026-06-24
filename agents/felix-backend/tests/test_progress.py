"""Progress module tests — PF gate logic, fast-unlock, facilitator override."""
import json
from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Enrolment
from src.db.models.curriculum import Exercise
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.models.submission import EvaluationResult, PFSignal, Submission, SubmissionStatus
from src.db.uuidv7 import uuid7_str
from src.progress.service import recompute_progress_after_evaluation


async def _make_submission(
    db: AsyncSession,
    progress: ExerciseProgress,
    enrolment: Enrolment,
    exercise: Exercise,
    attempt_number: int = 1,
) -> Submission:
    """Create a minimal Submission record required as FK parent for EvaluationResult."""
    sub = Submission(
        id=uuid7_str(),
        exercise_progress_id=progress.id,
        enrolment_id=enrolment.id,
        exercise_id=exercise.id,
        attempt_number=attempt_number,
        payload=json.dumps({"schema_version": "1.0"}),
        status=SubmissionStatus.evaluated,
        idempotency_key=uuid7_str(),
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(sub)
    await db.flush()
    return sub


def _make_eval(submission_id: str, **kwargs) -> EvaluationResult:
    defaults = {
        "submission_id": submission_id,
        "schema_version": "1.0",
        "ran": True,
        "overall_score": 0.5,
        "productive_failure_signal": PFSignal.productive,
        "detected_approach": "approach.basic",
        "confidence": 0.8,
        "passed": False,
        "judge_model": "claude-sonnet-4-6",
        "judge_escalated": False,
        "evaluated_at": datetime.now(timezone.utc),
    }
    defaults.update(kwargs)
    return EvaluationResult(id=uuid7_str(), **defaults)


@pytest.mark.asyncio
async def test_gate_opens_after_two_genuine_attempts(
    db: AsyncSession,
    enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    """Gate requires min_attempts=2, min_distinct_approaches=2, min_exploration_seconds=300."""
    # Pre-condition: set exploration_seconds to satisfy that gate
    progress.exploration_seconds = 400

    # First productive submission → phase stays exploring (need 2 genuine)
    sub1 = await _make_submission(db, progress, enrolment, exercise, attempt_number=1)
    e1 = _make_eval(sub1.id, detected_approach="approach.basic")
    db.add(e1)
    await db.flush()
    await recompute_progress_after_evaluation(db, enrolment.id, exercise.id, e1)
    await db.flush()
    assert progress.phase == ExercisePhase.exploring
    assert progress.attempts_genuine == 1

    # Second productive submission with different approach → gate should open
    sub2 = await _make_submission(db, progress, enrolment, exercise, attempt_number=2)
    e2 = _make_eval(sub2.id, detected_approach="approach.multi-tool")
    db.add(e2)
    await db.flush()
    await recompute_progress_after_evaluation(db, enrolment.id, exercise.id, e2)
    await db.flush()

    assert progress.phase == ExercisePhase.consolidation_unlocked
    assert progress.unlocked_at is not None


@pytest.mark.asyncio
async def test_fast_unlock_on_first_pass(
    db: AsyncSession,
    enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    """First attempt passes with confidence ≥ 0.85 → fast-unlock."""
    assert exercise.allow_fast_unlock is True

    sub = await _make_submission(db, progress, enrolment, exercise)
    e = _make_eval(
        sub.id,
        passed=True,
        confidence=0.92,
        productive_failure_signal=PFSignal.productive,
    )
    db.add(e)
    await db.flush()
    await recompute_progress_after_evaluation(db, enrolment.id, exercise.id, e)
    await db.flush()

    assert progress.phase == ExercisePhase.consolidation_unlocked
    assert progress.explored is False  # fast-unlock → explored=False per ADR-004


@pytest.mark.asyncio
async def test_low_effort_does_not_count_as_genuine(
    db: AsyncSession,
    enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    progress.exploration_seconds = 400

    sub = await _make_submission(db, progress, enrolment, exercise)
    e = _make_eval(
        sub.id,
        productive_failure_signal=PFSignal.low_effort,
        passed=False,
        confidence=0.9,
    )
    db.add(e)
    await db.flush()
    await recompute_progress_after_evaluation(db, enrolment.id, exercise.id, e)
    await db.flush()

    assert progress.attempts_genuine == 0
    assert progress.phase == ExercisePhase.exploring


@pytest.mark.asyncio
async def test_gate_does_not_reopen_from_completed(
    db: AsyncSession,
    enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
):
    """Phase transitions are one-way: completed stays completed."""
    progress.phase = ExercisePhase.completed
    progress.exploration_seconds = 0  # reset so normal gate wouldn't fire

    sub = await _make_submission(db, progress, enrolment, exercise)
    e = _make_eval(sub.id, passed=True, confidence=0.95)
    db.add(e)
    await db.flush()
    await recompute_progress_after_evaluation(db, enrolment.id, exercise.id, e)
    await db.flush()

    assert progress.phase == ExercisePhase.completed


@pytest.mark.asyncio
async def test_facilitator_override_unlock(
    db: AsyncSession,
    enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
    facilitator,
):
    from src.progress.service import apply_facilitator_override

    result = await apply_facilitator_override(
        db,
        progress.id,
        "unlock_consolidation",
        "Pilot exception",
        facilitator,
    )
    assert result["phase"] == "consolidation_unlocked"
    assert result["explored"] is False  # flagged as bypass


@pytest.mark.asyncio
async def test_facilitator_override_requires_role(
    db: AsyncSession,
    enrolment,
    exercise: Exercise,
    progress: ExerciseProgress,
    learner,
):
    from src.lib.exceptions import forbidden
    from src.progress.service import apply_facilitator_override
    import fastapi

    with pytest.raises(fastapi.HTTPException) as exc_info:
        await apply_facilitator_override(
            db, progress.id, "unlock_consolidation", "reason", learner
        )
    assert exc_info.value.status_code == 403
