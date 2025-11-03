import pytest

from app.domain.common.email import Email
from app.domain.errors import ValidationFailed


def test_email_can_be_created():
    email = Email(value="test@example.com")
    assert email.value == "test@example.com"


def test_email_invalid_raises_validation_failed():
    with pytest.raises(ValidationFailed):
        Email(value="invalid_email")
