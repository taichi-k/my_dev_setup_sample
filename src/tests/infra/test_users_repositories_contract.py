import pytest

from app.domain.common.email import Email
from app.domain.errors import Conflict
from app.domain.users.user import User
from app.domain.users.user_age import UserAge
from app.infra.users.mock_users_repository import MockUsersRepository


def repo_contract(factory):
    repo = factory()

    assert repo.find_by_username("x") is None

    repo.save(User(username="A", age=UserAge(30), email=Email("a@example.com")))
    assert repo.find_by_username("A") == User(
        username="A", age=UserAge(30), email=Email("a@example.com")
    )

    with pytest.raises(Conflict):
        repo.save(User(username="A", age=UserAge(30), email=Email("x@example.com")))
    with pytest.raises(Conflict):
        repo.save(User(username="X", age=UserAge(30), email=Email("a@example.com")))


@pytest.mark.parametrize(
    "factory",
    [
        lambda: MockUsersRepository(),
    ],
)
def test_contract(factory):
    repo_contract(factory)
