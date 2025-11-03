from app.domain.common.email import Email
from app.domain.users.user import User, UserAge
from app.domain.users.users_repository import UsersRepository


class MockUsersRepository(UsersRepository):
    def __init__(self):
        self.users = [User(username="default", age=UserAge(30), email=Email("default@example.com"))]

    def save(self, user: User) -> None:
        self.users.append(user)

    def find_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user.username == username:
                return user
        return None
