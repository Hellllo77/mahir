from fastapi import APIRouter

from src.auth import schemas, service
from src.lib.deps import CurrentUser, DbDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.TokenResponse)
async def login(body: schemas.LoginRequest, db: DbDep):
    token, expires_in = await service.authenticate_local(db, body.email, body.password)
    return schemas.TokenResponse(access_token=token, token_type="bearer", expires_in=expires_in)


@router.get("/oidc/callback", response_model=schemas.TokenResponse)
async def oidc_callback(code: str, state: str, db: DbDep):
    token, expires_in = await service.exchange_oidc_code(db, code, state)
    return schemas.TokenResponse(access_token=token, token_type="bearer", expires_in=expires_in)


me_router = APIRouter(tags=["auth"])


@me_router.get("/me", response_model=schemas.Me)
async def get_me(db: DbDep, current_user: CurrentUser):
    return await service.get_me(db, current_user)
