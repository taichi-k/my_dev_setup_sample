from ...domain.common.email import Email
from ...domain.users.user import User
from ...domain.users.user_age import UserAge
from ...domain.users.users_repository import UsersRepository


class UsersService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    def create_user(
        self, username: str = "new_user", age: int = 0, email: str = "new_user@example.com"
    ) -> bool:
        user = User(username=username, age=UserAge(age), email=Email(email))
        self.repo.save(user)
        return True

    def get_user_by_username(self, username: str) -> User | None:
        return self.repo.find_by_username(username)
