import pytest

from app.application.users.users_service import UsersService
from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.user import User
from app.infra.users.mock_users_repository import MockUsersRepository


def test_create_user_succeed():
    service = UsersService(repo=MockUsersRepository())
    result = service.create_user()
    assert result is True


def test_create_user_fail_on_duplicate_username():
    service = UsersService(repo=MockUsersRepository())
    service.create_user("existing", 25, Email("existing@example.com"))
    with pytest.raises(Conflict):
        service.create_user("existing", 25, Email("new@example.com"))


def test_create_user_fail_on_duplicate_email():
    service = UsersService(repo=MockUsersRepository())
    service.create_user("user1", 25, Email("user1@example.com"))
    with pytest.raises(Conflict):
        service.create_user("user2", 30, Email("user1@example.com"))


def test_get_user_by_username_can_find_user():
    service = UsersService(repo=MockUsersRepository())
    service.create_user("new", 25, Email("new@example.com"))
    user: User | None = service.get_user_by_username("new")
    assert user is not None
    assert user.username == "new"
