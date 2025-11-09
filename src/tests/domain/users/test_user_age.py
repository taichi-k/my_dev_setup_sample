import pytest

from app.domain.errors import ValidationFailed
from app.domain.users.user_age import UserAge


def test_user_age_can_be_created() -> None:
    user_age = UserAge(value=30)
    assert user_age.value == 30


def test_user_age_negative_value_raises_validation_failed() -> None:
    with pytest.raises(ValidationFailed):
        UserAge(value=-5)


def test_user_age_too_high_raises_validation_failed() -> None:
    with pytest.raises(ValidationFailed):
        UserAge(value=150)
