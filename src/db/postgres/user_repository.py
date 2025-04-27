from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import UserCreate

from .models import User


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

    async def create(self, user: UserCreate, session: AsyncSession) -> None:
        try:
            new_user = User(email=user.email, password=user.password, full_name=user.full_name)
            session.add(new_user)
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc

    # async def update(self, user: UserUpdate, session: AsyncSession):
    #     pass

    # async def delete(self, user: str, session: AsyncSession):
    #     pass

    # async def get_user_list(self, session: AsyncSession):
    #     pass

def get_user_repository() -> UserRepository:
    return UserRepository()
