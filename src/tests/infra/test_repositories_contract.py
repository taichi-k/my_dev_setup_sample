import pytest

from app.domain.common.email import Email
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
    # 重複
    # with pytest.raises(Exception):
    #     repo.save(User(username="A", age=UserAge(30), email=Email("a@example.com")))


@pytest.mark.parametrize(
    "factory",
    [
        lambda: MockUsersRepository(),
    ],
)
def test_contract(factory):
    repo_contract(factory)
