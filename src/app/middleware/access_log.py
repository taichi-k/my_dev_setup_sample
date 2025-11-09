from __future__ import annotations

import logging
import time
from typing import Awaitable, Callable

from fastapi import Request, Response

log = logging.getLogger("app")


async def access_log_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start = time.perf_counter()
    resp: Response | None = None
    try:
        resp = await call_next(request)
        return resp
    finally:
        dur_ms = (time.perf_counter() - start) * 1000
        # 必要に応じてヘッダも拾える（例: X-Request-Id）
        ua = request.headers.get("user-agent", "-")
        xff = request.headers.get("x-forwarded-for", None)
        extra = {
            "extra": {
                "type": "access",
                "method": request.method,
                "path": request.url.path,
                "query": str(request.url.query) if request.url.query else "",
                "status": getattr(resp, "status_code", 0),
                "latency_ms": round(dur_ms, 1),
                "client_ip": (
                    xff.split(",")[0].strip()
                    if xff
                    else (request.client.host if request.client else "-")
                ),
                "user_agent": ua,
                "service": "app",
                "env": "dev",
            }
        }
        log.info("request_done", extra=extra)
