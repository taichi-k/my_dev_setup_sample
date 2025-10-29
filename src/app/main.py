from __future__ import annotations

import logging
import os

import sentry_sdk
from fastapi import Depends, FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .logging_conf import setup_logging
from .middleware_config import setup_middlewares

setup_logging()
log = logging.getLogger("app")

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN", ""),
    send_default_pii=True,
    traces_sample_rate=1.0,
    enable_logs=True,
)

app = FastAPI(title="FastAPI + Postgres + uv Starter")

# middlewareの設定
setup_middlewares(app)

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


@app.get("/error_log")
async def error_log() -> dict:
    try:
        division_by_zero = 1 / 0
    except ZeroDivisionError as e:
        log.error(
            "An error occurred",
            exc_info=e,
            extra={"extra": {"service": "app", "event": "error_log"}},
        )
        return {"message": "Error logged"}
    return {"message": division_by_zero}


@app.get("/")
async def root() -> dict:
    log.info("Root endpoint accessed", extra={"extra": {"service": "app", "event": "root_access"}})
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
    return {"message": "Logged messages to Sentry"}


@app.get("/sleep")
async def sleep_endpoint():
    import asyncio

    await asyncio.sleep(5)
    return {"message": "Slept for 5 seconds"}
