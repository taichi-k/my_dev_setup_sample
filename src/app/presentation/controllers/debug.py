import logging

from fastapi import APIRouter

router = APIRouter()
log = logging.getLogger("app")


@router.get("/sentry-debug")
async def trigger_error() -> dict:
    division_by_zero = 1 / 0
    return {"result": division_by_zero}


@router.get("/sleep")
async def sleep_endpoint() -> dict:
    import asyncio

    await asyncio.sleep(5)
    return {"message": "Slept for 5 seconds"}


@router.get("/")
async def debug_endpoint() -> dict:
    log.info(
        "This is a debug log for debugging purposes",
        extra={"extra": {"service": "app", "event": "debug_endpoint"}},
    )
    return {"message": "Debug log sent"}


@router.get("/error_log")
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
