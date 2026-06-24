"""One-shot admin seed — run from app root: python seed_admin.py"""
import asyncio

from sqlalchemy import select

from src.db.base import AsyncSessionLocal
from src.db.models.auth import Organization, User
from src.db.uuidv7 import uuid7_str
from src.lib.jwt import hash_password


async def seed() -> None:
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Organization).limit(1))
        org = result.scalar_one_or_none()

        if org is None:
            org = Organization(
                id=uuid7_str(),
                name="Mahir Pilot",
                slug="mahir-pilot",
                edition="co_worker",
                region="MY",
                status="active",
            )
            db.add(org)
            await db.flush()
            print(f"[seed] created org  id={org.id} slug={org.slug}")
        else:
            print(f"[seed] using org    id={org.id} slug={org.slug}")

        result = await db.execute(
            select(User).where(User.email == "davidfush@gmail.com")
        )
        existing = result.scalar_one_or_none()

        if existing is not None:
            print(f"[seed] user already exists id={existing.id} — no changes made")
        else:
            user = User(
                id=uuid7_str(),
                organization_id=org.id,
                email="davidfush@gmail.com",
                display_name="David",
                auth_provider="local",
                password_hash=hash_password("Jordan23!"),
                global_role="super_admin",
                status="active",
            )
            db.add(user)
            print(f"[seed] created user id={user.id} email={user.email} role={user.global_role}")

        await db.commit()
        print("[seed] done.")


asyncio.run(seed())
