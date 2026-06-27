"""FastAPI application — Mahir backend (ADR-001, ADR-005)."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.admin.router import router as admin_router
from src.auth.router import me_router, router as auth_router
from src.cohorts.router import router as cohorts_router
from src.config import settings
from src.curriculum.router import me_curriculum_router, router as curriculum_router
from src.progress.router import facilitator_router, router as progress_router
from src.submissions.router import router as submissions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Mahir Backend API",
    version="0.1.0",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz", tags=["ops"])
async def healthz():
    return {"status": "ok"}


v1 = FastAPI(title="Mahir API v1")

v1.include_router(admin_router)
v1.include_router(auth_router)
v1.include_router(me_router)
v1.include_router(me_curriculum_router)
v1.include_router(cohorts_router)
v1.include_router(curriculum_router)
v1.include_router(progress_router)
v1.include_router(facilitator_router)
v1.include_router(submissions_router)

app.mount(settings.api_v1_prefix, v1)
