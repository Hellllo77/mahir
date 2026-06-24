"""Submissions — intake, idempotency, async queue dispatch (ADR-003/005)."""
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_db
from src.db.models.auth import Cohort, Enrolment, User
from src.db.models.curriculum import Exercise
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.models.submission import EvaluationResult, Submission, SubmissionStatus
from src.db.uuidv7 import uuid7_str
from src.lib.exceptions import bad_request, conflict, forbidden, not_found
from src.lib.queue import enqueue_evaluation


async def submit(
    db: AsyncSession,
    exercise_id: str,
    payload: dict,
    artifact_refs: list | None,
    idempotency_key: str,
    user: User,
) -> dict:
    """Accept a submission; enqueue evaluation; return 202 Submission (ADR-003/005)."""
    # Idempotency: return existing submission if key already used
    existing = await db.execute(
        select(Submission).where(Submission.idempotency_key == idempotency_key)
    )
    dup = existing.scalar_one_or_none()
    if dup is not None:
        return _submission_to_dict(dup)

    # Resolve exercise + enrolment
    exercise_result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id, Exercise.deleted_at.is_(None))
    )
    exercise = exercise_result.scalar_one_or_none()
    if exercise is None:
        raise not_found("Exercise")

    enrolment = await _get_enrolment_for_exercise(db, exercise, user)

    # Get or create ExerciseProgress
    progress = await _get_or_create_progress(db, enrolment.id, exercise_id, user.id)

    # Increment attempt number
    prev_submissions = await db.execute(
        select(Submission).where(
            Submission.enrolment_id == enrolment.id,
            Submission.exercise_id == exercise_id,
        )
    )
    attempt_number = len(prev_submissions.scalars().all()) + 1

    submission = Submission(
        id=uuid7_str(),
        exercise_progress_id=progress.id,
        enrolment_id=enrolment.id,
        exercise_id=exercise_id,
        attempt_number=attempt_number,
        payload=json.dumps({**payload, "schema_version": payload.get("schema_version", "1.0")}),
        artifact_refs=json.dumps(artifact_refs) if artifact_refs else None,
        status=SubmissionStatus.queued,
        idempotency_key=idempotency_key,
        submitted_at=datetime.now(timezone.utc),
        created_by=user.id,
    )
    db.add(submission)
    await db.flush()

    # Dispatch async evaluation (ADR-005: API → Evaluator via Redis queue)
    enqueue_evaluation(submission.id)

    return _submission_to_dict(submission)


async def list_submissions(db: AsyncSession, exercise_id: str, user: User) -> list[dict]:
    """List caller's submissions for an exercise, newest first."""
    exercise_result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id, Exercise.deleted_at.is_(None))
    )
    exercise = exercise_result.scalar_one_or_none()
    if exercise is None:
        raise not_found("Exercise")

    enrolment = await _get_enrolment_for_exercise(db, exercise, user)

    result = await db.execute(
        select(Submission)
        .where(
            Submission.enrolment_id == enrolment.id,
            Submission.exercise_id == exercise_id,
        )
        .order_by(Submission.submitted_at.desc())
    )
    return [_submission_to_dict(s) for s in result.scalars().all()]


async def get_submission(db: AsyncSession, submission_id: str, user: User) -> dict:
    """Get a submission + evaluation result; enforce ownership."""
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    if submission is None:
        raise not_found("Submission")

    # Tenant isolation: submission enrolment must belong to current user
    enrolment_result = await db.execute(
        select(Enrolment).where(
            Enrolment.id == submission.enrolment_id,
            Enrolment.user_id == user.id,
        )
    )
    if enrolment_result.scalar_one_or_none() is None:
        raise forbidden()

    eval_result = None
    if submission.status == SubmissionStatus.evaluated:
        er = await db.execute(
            select(EvaluationResult).where(EvaluationResult.submission_id == submission_id)
        )
        eval_result = er.scalar_one_or_none()

    return _submission_detail_to_dict(submission, eval_result)


async def _get_enrolment_for_exercise(db: AsyncSession, exercise: Exercise, user: User) -> Enrolment:
    from src.db.models.curriculum import Module

    module_result = await db.execute(
        select(Module).where(Module.id == exercise.module_id, Module.deleted_at.is_(None))
    )
    module = module_result.scalar_one_or_none()
    if module is None:
        raise not_found("Module")

    enrolment_result = await db.execute(
        select(Enrolment)
        .join(Cohort, Cohort.id == Enrolment.cohort_id)
        .where(
            Enrolment.user_id == user.id,
            Cohort.curriculum_id == module.curriculum_id,
            Cohort.organization_id == user.organization_id,
            Enrolment.deleted_at.is_(None),
            Cohort.deleted_at.is_(None),
        )
    )
    enrolment = enrolment_result.scalar_one_or_none()
    if enrolment is None:
        raise forbidden("Not enrolled in a cohort for this exercise.")
    return enrolment


async def _get_or_create_progress(
    db: AsyncSession, enrolment_id: str, exercise_id: str, actor_id: str
) -> ExerciseProgress:
    result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.enrolment_id == enrolment_id,
            ExerciseProgress.exercise_id == exercise_id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    progress = result.scalar_one_or_none()
    if progress is None:
        progress = ExerciseProgress(
            id=uuid7_str(),
            enrolment_id=enrolment_id,
            exercise_id=exercise_id,
            phase=ExercisePhase.exploring,
            created_by=actor_id,
        )
        db.add(progress)
        await db.flush()
    elif progress.phase == ExercisePhase.not_started:
        progress.phase = ExercisePhase.exploring
        await db.flush()
    return progress


def _submission_to_dict(s: Submission) -> dict:
    return {
        "id": s.id,
        "exercise_id": s.exercise_id,
        "attempt_number": s.attempt_number,
        "status": s.status.value,
        "submitted_at": s.submitted_at.isoformat(),
    }


def _submission_detail_to_dict(s: Submission, er: EvaluationResult | None) -> dict:
    d = _submission_to_dict(s)
    if er is not None:
        d["result"] = {
            "submission_id": er.submission_id,
            "schema_version": er.schema_version,
            "ran": er.ran,
            "scenario_results": json.loads(er.scenario_results) if er.scenario_results else None,
            "rubric_scores": json.loads(er.rubric_scores) if er.rubric_scores else None,
            "overall_score": float(er.overall_score),
            "productive_failure_signal": er.productive_failure_signal.value,
            "detected_approach": er.detected_approach,
            "confidence": float(er.confidence) if er.confidence is not None else None,
            "passed": er.passed,
            "feedback_markdown": er.feedback_markdown,
            "judge_model": er.judge_model,
            "judge_escalated": er.judge_escalated,
            "usage": {
                "input_tokens": er.usage_input_tokens,
                "output_tokens": er.usage_output_tokens,
                "cache_read_input_tokens": er.usage_cache_read_tokens,
            } if er.usage_input_tokens is not None else None,
            "cost_micro_usd": er.cost_micro_usd,
            "evaluated_at": er.evaluated_at.isoformat(),
        }
    else:
        d["result"] = None
    return d
