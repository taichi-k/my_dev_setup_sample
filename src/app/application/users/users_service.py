from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.policies import UniquenessResult, UserUniquenessPolicy
from app.domain.users.repository import UsersRepository
from app.domain.users.user import User
from app.domain.users.user_age import UserAge


class DefaultUserUniquenessPolicy(UserUniquenessPolicy):
    def __init__(self, repo: UsersRepository):
        self.repo = repo

    async def evaluate(self, username: str, email: Email) -> UniquenessResult:
        errors: list[str] = []
        if await self.repo.exists_by_username(username):
            errors.append(f"Username '{username}' is already taken.")
        if await self.repo.exists_by_email(email):
            errors.append(f"Email '{email}' is already registered.")
        return UniquenessResult(ok=not errors, errors=errors)


class UsersService:
    def __init__(self, repo: UsersRepository, policy: UserUniquenessPolicy | None = None):
        self.repo = repo
        self.uniqueness_policy = policy or DefaultUserUniquenessPolicy(repo)

    async def create_user(
        self, username: str = "new_user", age: int = 0, email: Email = Email("new_user@example.com")
    ) -> bool:
        user = User(username=username, age=UserAge(age), email=email)
        result = await self.uniqueness_policy.evaluate(username=username, email=email)
        if not result.ok:
            raise Conflict(", ".join(result.errors))
        await self.repo.save(user)
        return True

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.repo.find_by_username(username)
