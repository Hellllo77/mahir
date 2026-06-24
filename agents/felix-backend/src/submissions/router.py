from fastapi import APIRouter, Header, status

from src.lib.deps import CurrentUser, DbDep
from src.submissions import schemas, service

router = APIRouter(tags=["submissions"])


@router.post(
    "/exercises/{exercise_id}/submissions",
    response_model=schemas.SubmissionOut,
    status_code=status.HTTP_202_ACCEPTED,
)
async def submit(
    exercise_id: str,
    body: schemas.SubmissionCreate,
    db: DbDep,
    current_user: CurrentUser,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    return await service.submit(
        db,
        exercise_id,
        body.payload,
        body.artifact_refs,
        idempotency_key,
        current_user,
    )


@router.get("/exercises/{exercise_id}/submissions", response_model=list[schemas.SubmissionOut])
async def list_submissions(exercise_id: str, db: DbDep, current_user: CurrentUser):
    return await service.list_submissions(db, exercise_id, current_user)


@router.get("/submissions/{submission_id}", response_model=schemas.SubmissionDetailOut)
async def get_submission(submission_id: str, db: DbDep, current_user: CurrentUser):
    return await service.get_submission(db, submission_id, current_user)
