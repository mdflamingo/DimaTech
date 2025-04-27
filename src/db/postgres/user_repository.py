from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import AuthenticatedUser, UserInDB

from .models import User


class UserRepository:
    db_model = User

    async def get(self, user: AuthenticatedUser, session: AsyncSession):
        try:
            query = (
                select(self.db_model)
                .where(self.db_model.email == user.email)
                .limit(1)
            )
            result = await session.execute(query)
            user = result.scalar()
        except Exception as error:
            await session.rollback()
            raise error

        return user

    async def get_by_email(self, email: str, session: AsyncSession) -> UserInDB | None:
        try:
            query = (
                select(self.db_model)
                .where(self.db_model.email == email)
                .limit(1)
            )
            result = await session.execute(query)
            user = result.scalar()
        except Exception as error:
            await session.rollback()
            raise error
        if user:
            return UserInDB(**user.__dict__)
        return None


def get_user_repository() -> UserRepository:
    return UserRepository()
