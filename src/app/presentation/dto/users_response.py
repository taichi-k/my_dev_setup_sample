from typing import Any

from pydantic import BaseModel, Field


class CreateUserResponse(BaseModel):
    result: str


class GetUserResponse(BaseModel):
    username: str | None
    age: int | None
    email: str | None


class ErrorPayload(BaseModel):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
    retryable: bool


class ErrorResponse(BaseModel):
    error: ErrorPayload
