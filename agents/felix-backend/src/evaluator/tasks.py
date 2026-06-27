"""RQ task: full evaluation pipeline for a submission (ADR-003 + ADR-005)."""
import asyncio
import json
import logging
from datetime import datetime, timezone

from src.db.base import AsyncSessionLocal
from src.db.models.curriculum import ApproachTaxonomy, Exercise, RubricCriterion, Scenario
from src.db.models.submission import EvaluationResult, PFSignal, Submission, SubmissionStatus
from src.evaluator.judge import judge_submission
from src.evaluator.sandbox import run_sandbox
from src.progress.service import recompute_progress_after_evaluation

log = logging.getLogger(__name__)


async def reset_stuck_running_submissions() -> int:
    """On worker startup: flip any submission stuck in 'running' for >5 min to 'failed'.

    Guards against submissions orphaned when a previous worker process died mid-job.
    Returns the number of rows updated.
    """
    from sqlalchemy import text
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            text(
                "UPDATE submissions SET status = 'failed', updated_at = NOW() "
                "WHERE status = 'running' AND updated_at < NOW() - INTERVAL '5 minutes'"
            )
        )
        await db.commit()
        count = result.rowcount
        if count:
            log.warning("reset_stuck_running_submissions: reset %d stuck submission(s) to failed", count)
        return count


def run_evaluation(submission_id: str) -> None:
    """RQ entry point — runs in a worker process via asyncio.run()."""
    asyncio.run(_evaluate_async(submission_id))


async def _evaluate_async(submission_id: str) -> None:
    from src.db.base import engine
    await engine.dispose()  # asyncpg pools are loop-bound; dispose before each RQ job so new connections bind to this loop
    async with AsyncSessionLocal() as db:
        try:
            await _pipeline(db, submission_id)
            await db.commit()
        except Exception:
            await db.rollback()
            log.exception("Evaluation pipeline failed for submission %s", submission_id)
            await _mark_failed(submission_id)
            raise


async def _pipeline(db, submission_id: str) -> None:
    from sqlalchemy import select

    sub_r = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = sub_r.scalar_one_or_none()
    if submission is None:
        raise ValueError(f"Submission {submission_id} not found")

    submission.status = SubmissionStatus.running
    await db.flush()

    ex_r = await db.execute(select(Exercise).where(Exercise.id == submission.exercise_id))
    exercise = ex_r.scalar_one_or_none()
    if exercise is None:
        raise ValueError(f"Exercise {submission.exercise_id} not found")

    sc_r = await db.execute(
        select(Scenario).where(
            Scenario.exercise_id == exercise.id, Scenario.deleted_at.is_(None)
        )
    )
    scenarios = sc_r.scalars().all()

    rb_r = await db.execute(
        select(RubricCriterion).where(
            RubricCriterion.exercise_id == exercise.id, RubricCriterion.deleted_at.is_(None)
        )
    )
    rubric_criteria = rb_r.scalars().all()

    ap_r = await db.execute(
        select(ApproachTaxonomy).where(ApproachTaxonomy.exercise_id == exercise.id)
    )
    approaches = ap_r.scalars().all()

    # Stage 1: deterministic sandbox
    payload = json.loads(submission.payload)
    build_spec = json.loads(exercise.build_spec) if exercise.build_spec else {}
    sandbox_result = run_sandbox(
        payload,
        [_scenario_dict(s) for s in scenarios],
        build_spec,
    )

    # Stage 2: LLM judge (sync Anthropic calls — worker process only)
    judge_result, meta = judge_submission(
        submission_payload=payload,
        transcript_bundle=sandbox_result.transcript_bundle,
        scenarios=[_scenario_dict(s) for s in scenarios],
        rubric_criteria=[_rubric_dict(c) for c in rubric_criteria],
        exercise_prompt=exercise.prompt_markdown or "",
        approach_codes=[a.code for a in approaches],
    )

    now = datetime.now(timezone.utc)

    eval_result = EvaluationResult(
        submission_id=submission_id,
        schema_version=judge_result.schema_version,
        ran=judge_result.ran,
        scenario_results=json.dumps([r.model_dump() for r in judge_result.scenario_results]),
        rubric_scores=json.dumps([r.model_dump() for r in judge_result.rubric_scores]),
        overall_score=judge_result.overall_score,
        productive_failure_signal=PFSignal(judge_result.productive_failure_signal),
        detected_approach=judge_result.detected_approach,
        confidence=judge_result.confidence,
        passed=judge_result.passed,
        feedback_markdown=judge_result.feedback_markdown,
        judge_model=meta["judge_model"],
        judge_escalated=meta["escalated"],
        usage_input_tokens=meta["usage_input_tokens"],
        usage_output_tokens=meta["usage_output_tokens"],
        usage_cache_read_tokens=meta["usage_cache_read_tokens"],
        cost_micro_usd=meta["cost_micro_usd"],
        evaluated_at=now,
    )
    db.add(eval_result)
    await db.flush()

    submission.status = SubmissionStatus.evaluated
    await db.flush()

    # PF gate recompute — always post-evaluation, never at submit time (ADR-004)
    await recompute_progress_after_evaluation(
        db, submission.enrolment_id, submission.exercise_id, eval_result
    )


async def _mark_failed(submission_id: str) -> None:
    from sqlalchemy import update
    async with AsyncSessionLocal() as db:
        try:
            await db.execute(
                update(Submission)
                .where(Submission.id == submission_id)
                .values(status=SubmissionStatus.failed)
            )
            await db.commit()
        except Exception:
            log.exception("Could not mark submission %s as failed", submission_id)


def _scenario_dict(s: Scenario) -> dict:
    return {
        "id": s.id,
        "name": s.name,
        "input_payload": json.loads(s.input_payload) if s.input_payload else {},
        "assertions": json.loads(s.assertions) if s.assertions else {},
        "weight": float(s.weight) if s.weight is not None else 1.0,
    }


def _rubric_dict(c: RubricCriterion) -> dict:
    return {
        "code": c.code,
        "description": c.description,
        "weight": float(c.weight) if c.weight is not None else 1.0,
        "guidance_markdown": c.guidance_markdown,
    }
