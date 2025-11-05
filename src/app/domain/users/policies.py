from dataclasses import dataclass

from app.domain.common.email import Email
from app.domain.users.repository import UsersRepository


@dataclass
class UniquenessResult:
    ok: bool
    errors: list[str]


class UserUniquenessPolicy:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def evaluate(self, username: str, email: Email) -> UniquenessResult:
        errors: list[str] = []
        if self.repo.exists_by_username(username):
            errors.append(f"Username '{username}' is already taken.")
        if self.repo.exists_by_email(email):
            errors.append(f"Email '{email}' is already registered.")
        return UniquenessResult(ok=not errors, errors=errors)
