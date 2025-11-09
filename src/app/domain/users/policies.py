from dataclasses import dataclass
from typing import Protocol

from app.domain.common.email import Email


@dataclass
class UniquenessResult:
    ok: bool
    errors: list[str]


class UserUniquenessPolicy(Protocol):
    async def evaluate(self, username: str, email: Email) -> UniquenessResult: ...
