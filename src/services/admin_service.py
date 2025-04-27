from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres.admin_repository import AdminRepository, get_admin_repository

from src.models.user import AuthenticatedUser


@dataclass
class AdminService:
    admin_repository: AdminRepository

    async def auth(
        self, user: AuthenticatedUser, session: AsyncSession
    ) -> AuthenticatedUser | None:
        admin_in_db = await self.admin_repository.get_by_email(user.email, session)

        if admin_in_db and admin_in_db.check_password(user.password):
            return user


def get_user_service(
    admin_repository: AdminRepository = Depends(get_admin_repository),
) -> AdminService:
    return AdminService(admin_repository=admin_repository)
