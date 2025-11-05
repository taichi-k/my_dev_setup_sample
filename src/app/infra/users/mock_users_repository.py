from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.repository import UsersRepository
from app.domain.users.user import User, UserAge


class MockUsersRepository(UsersRepository):
    def __init__(self):
        self.users = [User(username="default", age=UserAge(30), email=Email("default@example.com"))]

    def save(self, user: User) -> None:
        if self.exists_by_username(user.username):
            raise Conflict("User already exists")
        if self.exists_by_email(user.email):
            raise Conflict("Email already exists")
        self.users.append(user)

    def find_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user.username == username:
                return user
        return None

    def exists_by_username(self, username: str) -> bool:
        return any(user.username == username for user in self.users)

    def exists_by_email(self, email: Email) -> bool:
        return any(user.email == email for user in self.users)
