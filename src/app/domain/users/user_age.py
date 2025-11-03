from dataclasses import dataclass

from app.domain.errors import ValidationFailed


@dataclass(frozen=True)
class UserAge:
    value: int

    def __post_init__(self):
        if not (0 <= self.value <= 130):
            raise ValidationFailed(field="Age", reason="Age must be between 0 and 130")
