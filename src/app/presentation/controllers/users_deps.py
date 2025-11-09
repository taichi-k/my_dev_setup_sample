from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.users.users_service import UsersService
from app.infra.db.core import get_session
from app.infra.repositories.sqlalchemy_users_repository import SQLAlchemyUsersRepository


async def get_users_service(
    session: AsyncSession = Depends(get_session),
) -> UsersService:
    repo = SQLAlchemyUsersRepository(session)
    return UsersService(repo)
