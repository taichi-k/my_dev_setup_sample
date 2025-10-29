from __future__ import annotations

import os

import sentry_sdk
from fastapi import Depends, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    traces_sample_rate=1.0,
    enable_logs=True,
)

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


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0
    return {"result": division_by_zero}


@app.get("/sentry-log")
async def log_messages():
    sentry_sdk.logger.info("This is an info log message")
    sentry_sdk.logger.warning("This is a warning message")
    sentry_sdk.logger.error("This is an error message")


@app.get("/sleep")
async def sleep_endpoint():
    import asyncio

    await asyncio.sleep(5)
    return {"message": "Slept for 5 seconds"}
