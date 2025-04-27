from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Account, User


class UserRepository:
    db_model = User

    async def get_by_email(self, email: str, session: AsyncSession) -> User | None:
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

        return user if user else None


def get_user_repository() -> UserRepository:
    return UserRepository()
