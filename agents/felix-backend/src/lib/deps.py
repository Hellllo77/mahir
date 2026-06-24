"""FastAPI dependency injectors — DB session + current user resolution."""
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_db
from src.db.models.auth import User, UserStatus
from src.lib.exceptions import unauthorized
from src.lib.jwt import decode_access_token

security = HTTPBearer()

DbDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: DbDep,
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError:
        raise unauthorized()

    user_id: str = payload.get("sub")
    if not user_id:
        raise unauthorized()

    result = await db.execute(
        select(User).where(User.id == user_id, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()
    if user is None or user.status == UserStatus.deactivated:
        raise unauthorized("User account not found or deactivated.")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
