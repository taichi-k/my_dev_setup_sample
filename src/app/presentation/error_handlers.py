from __future__ import annotations

from typing import Any, Mapping

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.errors import (
    Conflict,
    DomainError,
    EntityNotFound,
    ExternalServiceError,
    PermissionDenied,
    ValidationFailed,
)


def register_error_handlers(app: FastAPI) -> None:
    """Register shared exception handlers for domain-level errors."""

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        response_status = _status_code_for(exc)
        payload: Mapping[str, Any] = {
            "code": exc.code,
            "message": exc.message,
            "details": exc.details or {},
            "retryable": exc.retryable,
        }
        return JSONResponse(status_code=response_status, content={"error": payload})


def _status_code_for(error: DomainError) -> int:
    if isinstance(error, Conflict):
        return status.HTTP_409_CONFLICT
    if isinstance(error, EntityNotFound):
        return status.HTTP_404_NOT_FOUND
    if isinstance(error, ValidationFailed):
        return status.HTTP_400_BAD_REQUEST
    if isinstance(error, PermissionDenied):
        return status.HTTP_403_FORBIDDEN
    if isinstance(error, ExternalServiceError):
        return status.HTTP_502_BAD_GATEWAY
    return status.HTTP_500_INTERNAL_SERVER_ERROR
