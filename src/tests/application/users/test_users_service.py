from app.application.users.users_service import UsersService
from app.domain.users.user import User
from app.infra.users.mock_users_repository import MockUsersRepository


def test_create_user_succeed():
    service = UsersService(repo=MockUsersRepository())
    result = service.create_user()
    assert result is True


def test_get_user_by_username_can_find_user():
    service = UsersService(repo=MockUsersRepository())
    service.create_user("new", 25, "new@example.com")
    user: User | None = service.get_user_by_username("new")
    assert user is not None
    assert user.username == "new"
