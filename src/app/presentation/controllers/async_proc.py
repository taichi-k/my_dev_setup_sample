from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.infra.messaging.kafka_client import get_async_job_publisher

router = APIRouter()


@router.get("/async_proc")
async def trigger_async_processing() -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    publisher = get_async_job_publisher()

    try:
        await run_in_threadpool(publisher.publish_timestamp, timestamp)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail="Failed to queue async job") from exc

    return {"status": "queued", "timestamp": timestamp}
