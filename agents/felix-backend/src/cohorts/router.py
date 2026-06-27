from fastapi import APIRouter, Query, Response, status

from src.cohorts import schemas, service
from src.lib.deps import CurrentUser, DbDep

router = APIRouter(tags=["cohorts"])


@router.get("/cohorts", response_model=list[schemas.CohortSummary])
async def list_cohorts(db: DbDep, current_user: CurrentUser):
    return await service.list_cohorts(db, current_user)


@router.post("/cohorts", response_model=schemas.CohortDetail, status_code=status.HTTP_201_CREATED)
async def create_cohort(payload: schemas.CohortCreate, db: DbDep, current_user: CurrentUser):
    return await service.create_cohort(db, current_user, payload)


@router.get("/cohorts/{cohort_id}", response_model=schemas.CohortDetail)
async def get_cohort(cohort_id: str, db: DbDep, current_user: CurrentUser):
    return await service.get_cohort(db, current_user, cohort_id)


@router.patch("/cohorts/{cohort_id}", response_model=schemas.CohortDetail)
async def update_cohort(cohort_id: str, payload: schemas.CohortUpdate, db: DbDep, current_user: CurrentUser):
    return await service.update_cohort(db, current_user, cohort_id, payload.status, payload.name, payload.description)


@router.get("/cohorts/{cohort_id}/invite-link", response_model=schemas.InviteLink)
async def get_invite_link(cohort_id: str, db: DbDep, current_user: CurrentUser):
    return await service.get_invite_link(db, current_user, cohort_id)


@router.delete("/cohorts/{cohort_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cohort(
    cohort_id: str,
    force: bool = Query(False),
    db: DbDep = None,
    current_user: CurrentUser = None,
):
    await service.delete_cohort(db, cohort_id, current_user, force=force)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/cohorts/{cohort_id}/invite/send",
    response_model=schemas.InviteSendResult,
)
async def send_invites(
    cohort_id: str,
    body: schemas.InviteSendRequest,
    db: DbDep = None,
    current_user: CurrentUser = None,
):
    return await service.send_invites_manual(db, cohort_id, body.emails, current_user)


@router.post(
    "/cohorts/{cohort_id}/enrol",
    response_model=schemas.EnrolResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["cohorts"],
)
async def enrol_student(
    cohort_id: str,
    token: str = Query(...),
    payload: schemas.EnrolRequest = ...,
    db: DbDep = ...,
):
    return await service.enrol_student(db, cohort_id, token, payload)
