from fastapi import APIRouter

from src.curriculum import schemas, service
from src.lib.deps import CurrentUser, DbDep

router = APIRouter(tags=["curriculum"])


@router.get("/cohorts/{cohort_id}/modules", response_model=list[schemas.ModuleOut])
async def list_modules(cohort_id: str, db: DbDep, current_user: CurrentUser):
    return await service.list_modules(db, cohort_id, current_user)


@router.get("/exercises/{exercise_id}", response_model=schemas.ExerciseOut)
async def get_exercise(exercise_id: str, db: DbDep, current_user: CurrentUser):
    return await service.get_exercise(db, exercise_id, current_user)


@router.get("/exercises/{exercise_id}/consolidation", response_model=schemas.ConsolidationContentOut)
async def get_consolidation(exercise_id: str, db: DbDep, current_user: CurrentUser):
    return await service.get_consolidation(db, exercise_id, current_user)
