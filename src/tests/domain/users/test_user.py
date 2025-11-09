import pytest

from app.domain.common.email import Email
from app.domain.errors import ValidationFailed
from app.domain.users.user import User
from app.domain.users.user_age import UserAge


def test_user_can_be_created() -> None:
    user = User(username="testuser", age=UserAge(21), email=Email("testuser@example.com"))
    assert user.username == "testuser"
    assert user.age == UserAge(21)
    assert user.email == Email("testuser@example.com")


def test_user_invalid_age_raises_value_error() -> None:
    with pytest.raises(ValidationFailed):
        User(username="testuser", age=UserAge(150), email=Email("testuser@example.com"))


def test_user_invalid_email_raises_validation_failed() -> None:
    with pytest.raises(ValidationFailed):
        User(username="testuser", age=UserAge(21), email=Email("invalid-email"))
