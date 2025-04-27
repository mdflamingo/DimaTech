from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.user_repository import UserRepository, get_user_repository
from src.models.user import AuthenticatedUser


@dataclass
class AdminService:
    user_repository: UserRepository

    async def auth(self, user: AuthenticatedUser, session: AsyncSession) -> AuthenticatedUser | None:
        user_in_db = await self.user_repository.get_by_email(user.email, session)

        if user_in_db and user_in_db.check_password(user.password):
            return user


def get_user_service(user_repository: UserRepository = Depends(get_user_repository)) -> AdminService:
    return AdminService(user_repository=user_repository)
