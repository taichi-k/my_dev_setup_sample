import logging
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.common.email import Email
from app.domain.errors import Conflict, ExternalServiceError
from app.domain.users.repository import UsersRepository
from app.domain.users.user import User, UserAge
from app.infra.db.models.user_model import UserModel

log = logging.getLogger("app")


class SQLAlchemyUsersRepository(UsersRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_users(self) -> Sequence[User]:
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return [
            User(
                username=user_model.username,
                age=UserAge(user_model.age),
                email=Email(user_model.email),
            )
            for user_model in users
        ]

    async def save(self, user: User) -> None:
        user_model = UserModel(
            username=user.username,
            age=user.age.value,
            email=user.email.value,
        )
        try:
            self.session.add(user_model)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise Conflict("User or email already exists") from e
        except Exception as e:
            await self.session.rollback()
            log.error(f"Unexpected error when saving user: {e}")
            raise ExternalServiceError(
                __class__.__name__, "Failed to save user due to an unexpected error"
            ) from e

    async def find_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.username == username))
        user_model = result.scalar_one_or_none()
        if user_model is None:
            return None
        return User(
            username=user_model.username, age=UserAge(user_model.age), email=Email(user_model.email)
        )

    async def exists_by_username(self, username: str) -> bool:
        result = await self.session.execute(select(UserModel).where(UserModel.username == username))
        return result.scalar_one_or_none() is not None

    async def exists_by_email(self, email: Email) -> bool:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email.value))
        return result.scalar_one_or_none() is not None
