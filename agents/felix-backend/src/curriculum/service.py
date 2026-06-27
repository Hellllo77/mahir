"""Curriculum Engine — module/exercise delivery + PF-gated consolidation (ADR-004)."""
import json

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.db.models.auth import Cohort, Enrolment, User, UserGlobalRole
from src.db.models.curriculum import ConsolidationContent, Exercise, Module
from src.db.models.progress import ExercisePhase, ExerciseProgress
from src.lib.exceptions import forbidden, not_found, phase_locked
from src.lib.tenant import assert_cohort_access

_ADMIN_ROLES = {UserGlobalRole.super_admin, UserGlobalRole.org_admin, UserGlobalRole.facilitator}


async def list_modules(db: AsyncSession, cohort_id: str, user: User) -> list[dict]:
    """Return ordered modules for the cohort's pinned curriculum (tenant-scoped)."""
    cohort = await assert_cohort_access(db, cohort_id, user)

    enrolment_result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.user_id == user.id,
            Enrolment.deleted_at.is_(None),
        )
    )
    enrolment = enrolment_result.scalar_one_or_none()
    if enrolment is None and user.global_role not in _ADMIN_ROLES:
        raise forbidden("Not enrolled in this cohort.")

    result = await db.execute(
        select(Module)
        .where(Module.curriculum_id == cohort.curriculum_id, Module.deleted_at.is_(None))
        .options(selectinload(Module.exercises))
        .order_by(Module.sequence_index)
    )
    modules = result.scalars().all()

    # Fetch progress if the user has an enrolment; admins without one see not_started
    progress_map: dict[str, str] = {}
    if enrolment is not None:
        progress_result = await db.execute(
            select(ExerciseProgress).where(
                ExerciseProgress.enrolment_id == enrolment.id,
                ExerciseProgress.deleted_at.is_(None),
            )
        )
        progress_map = {p.exercise_id: p.phase.value for p in progress_result.scalars().all()}

    return [
        {
            "id": m.id,
            "title": m.title,
            "sequence_index": m.sequence_index,
            "summary_markdown": m.summary_markdown,
            "exercises": [
                {
                    "id": ex.id,
                    "title": ex.title,
                    "sequence_index": ex.sequence_index,
                    "phase": progress_map.get(ex.id, ExercisePhase.not_started.value),
                }
                for ex in sorted(m.exercises, key=lambda e: e.sequence_index)
                if ex.deleted_at is None
            ],
        }
        for m in modules
    ]


async def list_module_exercises(db: AsyncSession, cohort_id: str, module_id: str, user: User) -> list[dict]:
    """Return ordered exercises for a module, scoped to cohort access."""
    await assert_cohort_access(db, cohort_id, user)

    enrolment_result = await db.execute(
        select(Enrolment).where(
            Enrolment.cohort_id == cohort_id,
            Enrolment.user_id == user.id,
            Enrolment.deleted_at.is_(None),
        )
    )
    enrolment = enrolment_result.scalar_one_or_none()
    if enrolment is None and user.global_role not in _ADMIN_ROLES:
        raise forbidden("Not enrolled in this cohort.")

    result = await db.execute(
        select(Exercise)
        .where(Exercise.module_id == module_id, Exercise.deleted_at.is_(None))
        .order_by(Exercise.sequence_index)
    )
    exercises = result.scalars().all()

    is_admin = user.global_role in _ADMIN_ROLES
    return [
        {
            "id": ex.id,
            "module_id": ex.module_id,
            "title": ex.title,
            "sequence_index": ex.sequence_index,
            "prompt_markdown": ex.prompt_markdown,
            "facilitator_notes_markdown": ex.facilitator_notes_markdown if is_admin else None,
            "build_spec": json.loads(ex.build_spec) if ex.build_spec else {},
            "prerequisite_exercise_ids": json.loads(ex.prerequisite_exercise_ids or "[]"),
            "gate": {
                "min_attempts": ex.min_attempts,
                "min_distinct_approaches": ex.min_distinct_approaches,
                "min_exploration_seconds": ex.min_exploration_seconds,
                "allow_fast_unlock": ex.allow_fast_unlock,
            },
        }
        for ex in exercises
    ]


async def get_exercise(db: AsyncSession, exercise_id: str, user: User) -> dict:
    """Return exercise problem statement — never includes consolidation."""
    result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id, Exercise.deleted_at.is_(None))
    )
    exercise = result.scalar_one_or_none()
    if exercise is None:
        raise not_found("Exercise")

    if user.global_role not in _ADMIN_ROLES:
        await _assert_exercise_access(db, exercise, user)

    return {
        "id": exercise.id,
        "module_id": exercise.module_id,
        "title": exercise.title,
        "sequence_index": exercise.sequence_index,
        "prompt_markdown": exercise.prompt_markdown,
        "facilitator_notes_markdown": exercise.facilitator_notes_markdown if user.global_role in _ADMIN_ROLES else None,
        "build_spec": json.loads(exercise.build_spec) if exercise.build_spec else {},
        "prerequisite_exercise_ids": json.loads(exercise.prerequisite_exercise_ids or "[]"),
        "gate": {
            "min_attempts": exercise.min_attempts,
            "min_distinct_approaches": exercise.min_distinct_approaches,
            "min_exploration_seconds": exercise.min_exploration_seconds,
            "allow_fast_unlock": exercise.allow_fast_unlock,
        },
    }


async def get_consolidation(db: AsyncSession, exercise_id: str, user: User) -> dict:
    """Return consolidation content — 409 phase_locked unless gate passed (ADR-004 invariant 1)."""
    result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id, Exercise.deleted_at.is_(None))
    )
    exercise = result.scalar_one_or_none()
    if exercise is None:
        raise not_found("Exercise")

    enrolment = await _assert_exercise_access(db, exercise, user)

    # Gate check: phase must be consolidation_unlocked or completed
    progress_result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.enrolment_id == enrolment.id,
            ExerciseProgress.exercise_id == exercise_id,
            ExerciseProgress.deleted_at.is_(None),
        )
    )
    progress = progress_result.scalar_one_or_none()
    if progress is None or progress.phase not in (
        ExercisePhase.consolidation_unlocked,
        ExercisePhase.completed,
    ):
        raise phase_locked()

    content_result = await db.execute(
        select(ConsolidationContent).where(
            ConsolidationContent.exercise_id == exercise_id,
            ConsolidationContent.deleted_at.is_(None),
        )
    )
    content = content_result.scalar_one_or_none()
    if content is None:
        raise not_found("ConsolidationContent")

    return {
        "exercise_id": content.exercise_id,
        "body_markdown": content.body_markdown,
        "reference_build": json.loads(content.reference_build) if content.reference_build else None,
        "check_questions": json.loads(content.check_questions) if content.check_questions else None,
    }


async def _assert_exercise_access(db: AsyncSession, exercise: Exercise, user: User) -> Enrolment:
    """Verify user is enrolled in a cohort that pins a curriculum containing this exercise.
    Returns the enrolment. Raises 403 if not accessible."""
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
        .limit(1)
    )
    enrolment = enrolment_result.scalar_one_or_none()
    if enrolment is None:
        raise forbidden("Not enrolled in a cohort for this exercise.")
    return enrolment
