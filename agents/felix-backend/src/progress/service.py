"""Progress Store — PF phase state machine + facilitator gate overrides (ADR-004)."""
import json
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.auth import Cohort, Enrolment, User, UserGlobalRole, EnrolmentRole
from src.db.models.curriculum import Exercise
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.db.models.submission import EvaluationResult, PFSignal, Submission
from src.lib.exceptions import bad_request, forbidden, not_found


async def get_my_progress(db: AsyncSession, enrolment_id: str, user: User) -> list[dict]:
    """All ExerciseProgress records for the caller in an enrolment."""
    enrolment = await _assert_enrolment_ownership(db, enrolment_id, user)

    result = await db.execute(
        select(ExerciseProgress)
        .where(
            ExerciseProgress.enrolment_id == enrolment_id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    records = result.scalars().all()
    return [_progress_to_dict(p, db) for p in records]


_ADMIN_ROLES = {UserGlobalRole.super_admin, UserGlobalRole.org_admin, UserGlobalRole.facilitator}

_NOT_STARTED_PROGRESS = {
    "id": None,
    "exercise_id": None,
    "phase": ExercisePhase.not_started.value,
    "attempts_total": 0,
    "attempts_genuine": 0,
    "distinct_approaches": 0,
    "exploration_seconds": 0,
    "explored": False,
    "unlocked_at": None,
    "completed_at": None,
    "mastery_score": None,
}


async def get_exercise_progress(db: AsyncSession, exercise_id: str, user: User) -> dict:
    """PF phase state for a single (caller, exercise). Returns not_started if no record yet."""
    exercise_result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id, Exercise.deleted_at.is_(None))
    )
    exercise = exercise_result.scalar_one_or_none()
    if exercise is None:
        raise not_found("Exercise")

    if user.global_role in _ADMIN_ROLES:
        return {**_NOT_STARTED_PROGRESS, "exercise_id": exercise_id}

    enrolment = await _find_enrolment_for_exercise(db, exercise, user)

    progress_result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.enrolment_id == enrolment.id,
            ExerciseProgress.exercise_id == exercise_id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    progress = progress_result.scalar_one_or_none()
    if progress is None:
        return {**_NOT_STARTED_PROGRESS, "exercise_id": exercise_id}
    return _progress_to_dict(progress, exercise)


async def get_cohort_learner_progress(db: AsyncSession, cohort_id: str, user: User) -> list[dict]:
    """Cohort roster with PF signals — facilitator/admin only."""
    if user.global_role not in (UserGlobalRole.facilitator, UserGlobalRole.org_admin, UserGlobalRole.super_admin):
        cohort_enrolment = await _get_enrolment(db, cohort_id, user.id)
        if cohort_enrolment is None or cohort_enrolment.role != EnrolmentRole.facilitator:
            raise forbidden("Facilitator role required.")

    cohort_result = await db.execute(
        select(Cohort).where(
            Cohort.id == cohort_id,
            Cohort.organization_id == user.organization_id,
            Cohort.deleted_at.is_(None),
        )
    )
    cohort = cohort_result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort")

    enrolments_result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.deleted_at.is_(None),
        )
    )
    enrolments = enrolments_result.scalars().all()

    summaries = []
    for enrolment in enrolments:
        learner_result = await db.execute(
            select(User).where(User.id == enrolment.user_id)
        )
        learner = learner_result.scalar_one_or_none()
        if learner is None:
            continue

        progress_result = await db.execute(
            select(ExerciseProgress).where(
                ExerciseProgress.enrolment_id == enrolment.id,
                ExerciseProgress.deleted_at.is_(None),
            )
        )
        progress_records = progress_result.scalars().all()

        exercise_summaries = []
        for p in progress_records:
            latest_signal = await _get_latest_signal(db, enrolment.id, p.exercise_id)
            exercise_summaries.append({
                "progress_id": p.id,
                "exercise_id": p.exercise_id,
                "phase": p.phase.value,
                "attempts_total": p.attempts_total,
                "attempts_genuine": p.attempts_genuine,
                "explored": p.explored,
                "latest_signal": latest_signal,
            })

        summaries.append({
            "user_id": learner.id,
            "display_name": learner.display_name,
            "enrolment_id": enrolment.id,
            "exercises": exercise_summaries,
        })
    return summaries


async def get_member_progress(
    db: AsyncSession, cohort_id: str, target_user_id: str, user: User
) -> dict:
    """Per-member exercise progress drill-down — facilitator/admin only."""
    if user.global_role not in (UserGlobalRole.facilitator, UserGlobalRole.org_admin, UserGlobalRole.super_admin):
        cohort_enrolment = await _get_enrolment(db, cohort_id, user.id)
        if cohort_enrolment is None or cohort_enrolment.role != EnrolmentRole.facilitator:
            raise forbidden("Facilitator role required.")

    cohort_result = await db.execute(
        select(Cohort).where(
            Cohort.id == cohort_id,
            Cohort.organization_id == user.organization_id,
            Cohort.deleted_at.is_(None),
        )
    )
    cohort = cohort_result.scalar_one_or_none()
    if cohort is None:
        raise not_found("Cohort")

    learner_result = await db.execute(
        select(User).where(User.id == target_user_id, User.deleted_at.is_(None))
    )
    learner = learner_result.scalar_one_or_none()
    if learner is None:
        raise not_found("User")

    enrolment_result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.user_id == target_user_id,
            Enrolment.deleted_at.is_(None),
        )
    )
    enrolment = enrolment_result.scalar_one_or_none()
    if enrolment is None:
        raise not_found("Enrolment")

    progress_result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.enrolment_id == enrolment.id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    progress_records = progress_result.scalars().all()

    exercise_summaries = []
    for p in progress_records:
        latest_signal = await _get_latest_signal(db, enrolment.id, p.exercise_id)
        exercise_summaries.append({
            "progress_id": p.id,
            "exercise_id": p.exercise_id,
            "phase": p.phase.value,
            "attempts_total": p.attempts_total,
            "attempts_genuine": p.attempts_genuine,
            "explored": p.explored,
            "latest_signal": latest_signal,
        })

    return {
        "user_id": learner.id,
        "display_name": learner.display_name,
        "enrolment_id": enrolment.id,
        "exercises": exercise_summaries,
    }


async def apply_facilitator_override(
    db: AsyncSession, progress_id: str, action: str, reason: str, user: User
) -> dict:
    """Manually override a PF gate — audited (ADR-004: facilitator escape hatch)."""
    if user.global_role not in (UserGlobalRole.facilitator, UserGlobalRole.org_admin, UserGlobalRole.super_admin):
        raise forbidden("Facilitator role required for gate overrides.")

    progress_result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.id == progress_id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    progress = progress_result.scalar_one_or_none()
    if progress is None:
        raise not_found("ExerciseProgress")

    now = datetime.now(timezone.utc)
    override_record = {
        "action": action,
        "reason": reason,
        "actor_id": user.id,
        "at": now.isoformat(),
    }

    if action == "unlock_consolidation":
        progress.phase = ExercisePhase.consolidation_unlocked
        progress.unlocked_at = now
        progress.explored = False  # flagged as facilitator bypass
    elif action == "mark_completed":
        progress.phase = ExercisePhase.completed
        progress.completed_at = now
    elif action == "reset_exploring":
        progress.phase = ExercisePhase.exploring
    else:
        raise bad_request(f"Unknown action: {action}")

    progress.facilitator_override = json.dumps(override_record)
    progress.updated_by = user.id
    await db.flush()

    exercise_result = await db.execute(select(Exercise).where(Exercise.id == progress.exercise_id))
    exercise = exercise_result.scalar_one_or_none()
    return _progress_to_dict(progress, exercise)


async def recompute_progress_after_evaluation(
    db: AsyncSession, enrolment_id: str, exercise_id: str, result: EvaluationResult
) -> None:
    """Update ExerciseProgress after evaluation.completed event (ADR-004 gate logic).

    Called by the evaluator worker — NOT synchronous at submit time.
    """
    progress_result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.enrolment_id == enrolment_id,
            ExerciseProgress.exercise_id == exercise_id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    progress = progress_result.scalar_one_or_none()
    if progress is None:
        return

    exercise_result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id)
    )
    exercise = exercise_result.scalar_one_or_none()
    if exercise is None:
        return

    progress.attempts_total += 1

    # Genuine attempt: productive signal OR passed (ADR-004 gate invariant 2)
    is_genuine = (
        result.productive_failure_signal == PFSignal.productive or result.passed
    )
    if is_genuine:
        progress.attempts_genuine += 1

    # Variety: count distinct detected_approach codes across genuine submissions
    if is_genuine and result.detected_approach:
        progress.distinct_approaches = await _count_distinct_approaches(db, enrolment_id, exercise_id)

    # Update mastery score (best)
    if result.overall_score is not None:
        if progress.mastery_score is None or float(result.overall_score) > float(progress.mastery_score):
            progress.mastery_score = result.overall_score

    now = datetime.now(timezone.utc)

    # Gate evaluation — only from exploring phase
    if progress.phase == ExercisePhase.exploring:
        gate_passed = (
            progress.attempts_genuine >= exercise.min_attempts
            and progress.distinct_approaches >= exercise.min_distinct_approaches
            and progress.exploration_seconds >= exercise.min_exploration_seconds
        )
        # Fast-unlock: outright pass on attempt 1 with high confidence
        fast_unlock = (
            exercise.allow_fast_unlock
            and result.passed
            and result.confidence is not None
            and float(result.confidence) >= 0.85
            and progress.attempts_total == 1
        )
        if gate_passed or fast_unlock:
            progress.phase = ExercisePhase.consolidation_unlocked
            progress.unlocked_at = now
            progress.explored = not fast_unlock  # fast_unlock means explored=false (ADR-004)
    elif progress.phase == ExercisePhase.not_started:
        progress.phase = ExercisePhase.exploring

    await db.flush()


async def _count_distinct_approaches(db: AsyncSession, enrolment_id: str, exercise_id: str) -> int:
    """Count distinct detected_approach codes from genuine submissions (ADR-004 variety gate)."""
    result = await db.execute(
        select(EvaluationResult.detected_approach)
        .join(Submission, Submission.id == EvaluationResult.submission_id)
        .where(
            Submission.enrolment_id == enrolment_id,
            Submission.exercise_id == exercise_id,
            EvaluationResult.productive_failure_signal == PFSignal.productive,
            EvaluationResult.detected_approach.isnot(None),
        )
    )
    codes = {row[0] for row in result.all() if row[0]}
    return len(codes)


async def _get_latest_signal(db: AsyncSession, enrolment_id: str, exercise_id: str) -> str | None:
    result = await db.execute(
        select(EvaluationResult.productive_failure_signal)
        .join(Submission, Submission.id == EvaluationResult.submission_id)
        .where(
            Submission.enrolment_id == enrolment_id,
            Submission.exercise_id == exercise_id,
        )
        .order_by(Submission.submitted_at.desc())
        .limit(1)
    )
    row = result.scalar_one_or_none()
    return row.value if row else None


async def _assert_enrolment_ownership(db: AsyncSession, enrolment_id: str, user: User) -> Enrolment:
    result = await db.execute(
        select(Enrolment).where(
            Enrolment.id == enrolment_id,
            Enrolment.user_id == user.id,
            Enrolment.deleted_at.is_(None),
        )
    )
    enrolment = result.scalar_one_or_none()
    if enrolment is None:
        raise not_found("Enrolment")
    return enrolment


async def _get_enrolment(db: AsyncSession, cohort_id: str, user_id: str) -> Enrolment | None:
    result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.user_id == user_id,
            Enrolment.deleted_at.is_(None),
        )
    )
    return result.scalar_one_or_none()


async def _find_enrolment_for_exercise(db: AsyncSession, exercise: Exercise, user: User) -> Enrolment:
    from src.db.models.curriculum import Module

    module_result = await db.execute(select(Exercise).where(Exercise.id == exercise.id))
    ex = module_result.scalar_one_or_none()

    module_result = await db.execute(select(Module).where(Module.id == exercise.module_id))
    module = module_result.scalar_one_or_none()
    if module is None:
        raise not_found("Module")

    enrolment_result = await db.execute(
        select(Enrolment)
        .join(Cohort, Cohort.id == Enrolment.cohort_id)
        .where(
            Enrolment.user_id == user.id,
            Cohort.curriculum_id == module.curriculum_id,
            Enrolment.deleted_at.is_(None),
        )
        .limit(1)
    )
    enrolment = enrolment_result.scalar_one_or_none()
    if enrolment is None:
        raise forbidden("Not enrolled in a cohort for this exercise.")
    return enrolment


def _progress_to_dict(progress: ExerciseProgress, exercise: Exercise | None = None) -> dict:
    d = {
        "id": progress.id,
        "exercise_id": progress.exercise_id,
        "phase": progress.phase.value,
        "attempts_total": progress.attempts_total,
        "attempts_genuine": progress.attempts_genuine,
        "distinct_approaches": progress.distinct_approaches,
        "exploration_seconds": progress.exploration_seconds,
        "explored": progress.explored,
        "unlocked_at": progress.unlocked_at.isoformat() if progress.unlocked_at else None,
        "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
        "mastery_score": float(progress.mastery_score) if progress.mastery_score is not None else None,
    }
    if exercise is not None:
        d["gate"] = {
            "min_attempts": exercise.min_attempts,
            "min_distinct_approaches": exercise.min_distinct_approaches,
            "min_exploration_seconds": exercise.min_exploration_seconds,
            "allow_fast_unlock": exercise.allow_fast_unlock,
        }
    return d
