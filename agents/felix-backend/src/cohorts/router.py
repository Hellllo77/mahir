from fastapi import APIRouter, status

from src.cohorts import schemas, service
from src.lib.deps import CurrentUser, DbDep

router = APIRouter(tags=["cohorts"])


@router.get("/cohorts", response_model=list[schemas.CohortSummary])
async def list_cohorts(db: DbDep, current_user: CurrentUser):
    return await service.list_cohorts(db, current_user)


@router.post("/cohorts", response_model=schemas.CohortDetail, status_code=status.HTTP_201_CREATED)
async def create_cohort(payload: schemas.CohortCreate, db: DbDep, current_user: CurrentUser):
    return await service.create_cohort(db, current_user, payload)


@router.patch("/cohorts/{cohort_id}", response_model=schemas.CohortDetail)
async def update_cohort(cohort_id: str, payload: schemas.CohortUpdate, db: DbDep, current_user: CurrentUser):
    return await service.update_cohort(db, current_user, cohort_id, payload.status)


@router.get("/cohorts/{cohort_id}/invite-link", response_model=schemas.InviteLink)
async def get_invite_link(cohort_id: str, db: DbDep, current_user: CurrentUser):
    return await service.get_invite_link(db, current_user, cohort_id)
