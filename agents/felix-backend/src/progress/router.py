from fastapi import APIRouter, Query

from src.lib.deps import CurrentUser, DbDep
from src.progress import schemas, service

router = APIRouter(tags=["progress"])


@router.get("/me/progress", response_model=list[schemas.ExerciseProgressOut])
async def get_my_progress(
    enrolment_id: str = Query(...),
    db: DbDep = None,
    current_user: CurrentUser = None,
):
    return await service.get_my_progress(db, enrolment_id, current_user)


@router.get("/exercises/{exercise_id}/progress", response_model=schemas.ExerciseProgressOut)
async def get_exercise_progress(exercise_id: str, db: DbDep = None, current_user: CurrentUser = None):
    return await service.get_exercise_progress(db, exercise_id, current_user)


facilitator_router = APIRouter(prefix="/facilitator", tags=["facilitator"])


@facilitator_router.get(
    "/cohorts/{cohort_id}/learners", response_model=list[schemas.LearnerProgressSummary]
)
async def get_cohort_learners(cohort_id: str, db: DbDep = None, current_user: CurrentUser = None):
    return await service.get_cohort_learner_progress(db, cohort_id, current_user)


@facilitator_router.get(
    "/cohorts/{cohort_id}/members/{user_id}/progress",
    response_model=schemas.LearnerProgressSummary,
)
async def get_member_progress(cohort_id: str, user_id: str, db: DbDep = None, current_user: CurrentUser = None):
    return await service.get_member_progress(db, cohort_id, user_id, current_user)


@facilitator_router.post(
    "/progress/{progress_id}/override", response_model=schemas.ExerciseProgressOut
)
async def override_gate(
    progress_id: str,
    body: schemas.GateOverride,
    db: DbDep = None,
    current_user: CurrentUser = None,
):
    return await service.apply_facilitator_override(db, progress_id, body.action, body.reason, current_user)
