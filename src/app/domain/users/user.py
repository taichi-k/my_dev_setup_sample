from dataclasses import dataclass

from app.domain.common.email import Email
from app.domain.users.user_age import UserAge


@dataclass
class User:
    username: str
    age: UserAge
    email: Email
