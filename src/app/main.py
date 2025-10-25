from __future__ import annotations

from fastapi import Depends, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session

app = FastAPI(title="FastAPI + Postgres + uv Starter")

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",  # 変えたければ /_metrics など
    include_in_schema=False,
)


@app.get("/health")
async def health(session: AsyncSession = Depends(get_session)) -> dict:
    # DB 接続の簡易確認
    row = await session.execute(text("SELECT version()"))
    version = row.scalar_one()
    return {"ok": True, "db_version": version}


@app.get("/")
async def root() -> dict:
    return {"message": "hello from FastAPI on Dev Container!"}
