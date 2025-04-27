from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.postgres.admin_repository import AdminRepository, get_admin_repository

from src.db.postgres.user_repository import UserRepository, get_user_repository
from src.models.user import AuthenticatedUser


@dataclass
class AdminService:
    admin_repository: AdminRepository

    async def auth(self, user: AuthenticatedUser, session: AsyncSession) -> AuthenticatedUser | None:
        admin_in_db = await self.admin_repository.get_by_email(user.email, session)

        if admin_in_db and admin_in_db.check_password(user.password):
            return user

    async def create_user(user: UserCreate, session: AsyncSession):
        pass

    async def update_user(user: UserUpdate, session: AsyncSession):
        pass
    async def delete_user(user: str, session: AsyncSession):
        pass

def get_user_service(admin_repository: AdminRepository = Depends(get_admin_repository)) -> AdminService:
    return AdminService(admin_repository=admin_repository)
