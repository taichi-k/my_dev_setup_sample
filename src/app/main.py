from __future__ import annotations

import logging
import os

from fastapi import Depends, FastAPI
from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .core.logging_conf import setup_logging
from .db import get_session
from .middleware.middleware_config import setup_middlewares
from .observability.sentry import setup_sentry
from .presentation.controllers import debug, users_controller

setup_logging()
log = logging.getLogger("app")

setup_sentry()

OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317")
SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "app")
SERVICE_NAMESPACE = os.getenv("OTEL_SERVICE_NAMESPACE", "myproj")
DEPLOY_ENV = os.getenv("OTEL_DEPLOYMENT_ENVIRONMENT", "dev")

resource = Resource.create(
    {
        "service.name": SERVICE_NAME,
        "service.namespace": SERVICE_NAMESPACE,
        "deployment.environment": DEPLOY_ENV,
    }
)

metric_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=OTLP_ENDPOINT, insecure=True)
)
meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(meter_provider)  # ← 追加

meter = metrics.get_meter("app.http")
req_counter = meter.create_counter(
    "http_requests_total", description="Total number of HTTP requests"
)
req_latency = meter.create_histogram(
    "http_request_duration_seconds", description="HTTP request duration in seconds"
)

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True))
)
trace.set_tracer_provider(tracer_provider)

logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint=OTLP_ENDPOINT, insecure=True))
)
set_logger_provider(logger_provider)

otel_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
log.addHandler(otel_handler)

app = FastAPI(title="FastAPI + Postgres + uv Starter")
app.include_router(debug.router, prefix="/api/debug", tags=["debug"])
app.include_router(users_controller.router, prefix="/user", tags=["user"])

setup_middlewares(app)


@app.middleware("http")
async def metrics_middleware(request, call_next):
    import time

    start = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    finally:
        duration = time.perf_counter() - start
        attributes = {
            "path": request.url.path,
            "method": request.method,
            "status_code": getattr(response, "status_code", 500),
        }
        req_counter.add(1, attributes)
        req_latency.record(duration, attributes)


FastAPIInstrumentor.instrument_app(app)

try:
    SQLAlchemyInstrumentor().instrument()
except Exception as e:
    log.warning("SQLAlchemy instrumentation skipped: %s", e)


@app.get("/health")
async def health(session: AsyncSession = Depends(get_session)) -> dict:
    # DB 接続の簡易確認
    row = await session.execute(text("SELECT version()"))
    version = row.scalar_one()
    return {"ok": True, "db_version": version}


@app.get("/")
async def root() -> dict:
    log.info("Root endpoint accessed", extra={"extra": {"service": "app", "event": "root_access"}})
    return {"message": "Hello from FastAPI on Dev Container!"}
