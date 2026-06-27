from fastapi import APIRouter

from src.admin import schemas, service
from src.lib.deps import CurrentUser, DbDep

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/settings", response_model=schemas.SettingsOut)
async def get_settings(db: DbDep, current_user: CurrentUser):
    return await service.get_settings(db, current_user)


@router.put("/settings", response_model=schemas.SettingsOut)
async def update_settings(body: schemas.SettingsUpdate, db: DbDep, current_user: CurrentUser):
    return await service.update_settings(db, current_user, body)
