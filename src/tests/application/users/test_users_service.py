import pytest

from app.application.users.users_service import UsersService
from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.user import User
from app.infra.repositories.mock_users_repository import MockUsersRepository


@pytest.mark.asyncio
async def test_create_user_succeed() -> None:
    service = UsersService(repo=MockUsersRepository())
    result = await service.create_user()
    assert result is True


@pytest.mark.asyncio
async def test_create_user_fail_on_duplicate_username() -> None:
    service = UsersService(repo=MockUsersRepository())
    await service.create_user("existing", 25, Email("existing@example.com"))
    with pytest.raises(Conflict):
        await service.create_user("existing", 25, Email("new@example.com"))


@pytest.mark.asyncio
async def test_create_user_fail_on_duplicate_email() -> None:
    service = UsersService(repo=MockUsersRepository())
    await service.create_user("user1", 25, Email("user1@example.com"))
    with pytest.raises(Conflict):
        await service.create_user("user2", 30, Email("user1@example.com"))


@pytest.mark.asyncio
async def test_get_user_by_username_can_find_user() -> None:
    service = UsersService(repo=MockUsersRepository())
    await service.create_user("new", 25, Email("new@example.com"))
    user: User | None = await service.get_user_by_username("new")
    assert user is not None
    assert user.username == "new"
