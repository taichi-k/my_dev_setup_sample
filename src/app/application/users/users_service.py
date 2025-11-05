from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.policies import UserUniquenessPolicy
from app.domain.users.repository import UsersRepository
from app.domain.users.user import User
from app.domain.users.user_age import UserAge


class UsersService:
    def __init__(self, repo: UsersRepository):
        self.repo = repo
        self.uniqueness_policy = UserUniquenessPolicy(repo)

    def create_user(
        self, username: str = "new_user", age: int = 0, email: Email = Email("new_user@example.com")
    ) -> bool:
        user = User(username=username, age=UserAge(age), email=email)
        result = self.uniqueness_policy.evaluate(username=username, email=email)
        if not result.ok:
            raise Conflict(", ".join(result.errors))
        self.repo.save(user)
        return True

    def get_user_by_username(self, username: str) -> User | None:
        return self.repo.find_by_username(username)
