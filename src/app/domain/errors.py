# app/domain/errors.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass(eq=False)
class DomainError(Exception):
    code: str  # 安定したアプリ内コード（機械可読）
    message: str  # 人間可読
    details: Optional[Mapping[str, Any]] = None
    retryable: bool = False  # リトライ可否（キュー/リトライ戦略で使える）

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class EntityNotFound(DomainError):
    def __init__(self, entity: str, key: Any):
        super().__init__(
            code="entity_not_found",
            message=f"{entity} not found",
            details={"entity": entity, "key": key},
            retryable=False,
        )


class Conflict(DomainError):
    def __init__(self, reason: str, details: Optional[Mapping[str, Any]] = None):
        super().__init__("conflict", reason, details, retryable=False)


class ValidationFailed(DomainError):
    def __init__(self, field: str, reason: str, details: Optional[Mapping[str, Any]] = None):
        super().__init__("validation_failed", f"{field}: {reason}", details, retryable=False)


class PermissionDenied(DomainError):
    def __init__(self, reason: str = "permission denied"):
        super().__init__("permission_denied", reason, retryable=False)


class ExternalServiceError(DomainError):
    def __init__(self, service: str, reason: str, details: Optional[Mapping[str, Any]] = None):
        super().__init__("external_service_error", f"{service}: {reason}", details, retryable=True)
