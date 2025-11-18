# app/infrastructure/db/core.py
import os
from typing import AsyncIterator, Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}",
)


class Base(DeclarativeBase):
    pass


def make_engine(url: str) -> AsyncEngine:
    # 例: postgresql+asyncpg://user:pass@db:5432/app
    engine = create_async_engine(url, echo=False, pool_pre_ping=True)
    return engine


def make_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


def make_get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> Callable[[], AsyncIterator[AsyncSession]]:
    async def _get_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    return _get_session


engine = make_engine(DATABASE_URL)
SessionLocal = make_session_maker(engine)
get_session = make_get_session(SessionLocal)
