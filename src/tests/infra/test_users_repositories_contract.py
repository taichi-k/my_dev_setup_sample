import pytest

from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.user import User
from app.domain.users.user_age import UserAge
from app.infra.repositories.mock_users_repository import MockUsersRepository


async def repo_contract(factory):
    repo = factory()

    assert await repo.find_by_username("x") is None

    await repo.save(User(username="A", age=UserAge(30), email=Email("a@example.com")))
    assert await repo.find_by_username("A") == User(
        username="A", age=UserAge(30), email=Email("a@example.com")
    )

    with pytest.raises(Conflict):
        await repo.save(User(username="A", age=UserAge(30), email=Email("x@example.com")))
    with pytest.raises(Conflict):
        await repo.save(User(username="X", age=UserAge(30), email=Email("a@example.com")))


@pytest.mark.parametrize(
    "factory",
    [
        lambda: MockUsersRepository(),
    ],
)
@pytest.mark.asyncio
async def test_contract(factory):
    await repo_contract(factory)
