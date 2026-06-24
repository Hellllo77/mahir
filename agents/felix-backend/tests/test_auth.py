"""Auth module tests — local login, JWT decode, OIDC callback stub."""
import pytest
from httpx import AsyncClient

from src.db.models.auth import User, UserAuthProvider, UserGlobalRole
from src.db.uuidv7 import uuid7_str
from src.lib.jwt import create_access_token, decode_access_token, hash_password
from tests.conftest import make_auth_header, make_user


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, learner: User):
    resp = await client.post(
        "/v1/auth/login",
        json={"email": learner.email, "password": "password123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, learner: User):
    resp = await client.post(
        "/v1/auth/login",
        json={"email": learner.email, "password": "wrong"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_unknown_email(client: AsyncClient):
    resp = await client.post(
        "/v1/auth/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, learner: User):
    headers = make_auth_header(learner)
    resp = await client.get("/v1/me", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == learner.id
    assert data["email"] == learner.email


@pytest.mark.asyncio
async def test_get_me_no_auth(client: AsyncClient):
    resp = await client.get("/v1/me")
    assert resp.status_code == 401  # HTTPBearer returns 401 in FastAPI >=0.115


def test_jwt_round_trip():
    sub = str(uuid7_str())
    org_id = str(uuid7_str())
    token, expires_in = create_access_token(sub, org_id, "learner")
    assert expires_in > 0
    decoded = decode_access_token(token)
    assert decoded["sub"] == sub
    assert decoded["org_id"] == org_id
    assert decoded["role"] == "learner"


def test_hash_and_verify():
    from src.lib.jwt import verify_password
    pw = "hunter2"
    hashed = hash_password(pw)
    assert hashed != pw
    assert verify_password(pw, hashed)
    assert not verify_password("wrong", hashed)
