from fastapi import APIRouter

from src.cohorts import schemas, service
from src.lib.deps import CurrentUser, DbDep

router = APIRouter(tags=["cohorts"])


@router.get("/cohorts", response_model=list[schemas.CohortSummary])
async def list_cohorts(db: DbDep, current_user: CurrentUser):
    return await service.list_cohorts(db, current_user)
