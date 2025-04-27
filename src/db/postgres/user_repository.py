from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from werkzeug.security import generate_password_hash

from src.models.account import Account
from src.models.user import UserCreate, UserList, UserUpdate

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

    async def update(self, email: str, user: UserUpdate, session: AsyncSession) -> None:
        try:
            update_values = user.__dict__

            if 'password' in update_values and update_values['password']:
                update_values['password'] = generate_password_hash(update_values['password'])
            query = (
                update(self.db_model)
                .where(self.db_model.email == email)
                .values(**update_values)
            )
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                raise ValueError(f"Not found {self.db_model.__name__} with email: {email}")
        except Exception as exc:
            await session.rollback()
            raise exc

    async def delete(self, email: str, session: AsyncSession):
        try:
            query = delete(self.db_model).where(self.db_model.email == email)
            result = await session.execute(query)
            await session.commit()

            if result.rowcount == 0:
                raise ValueError(f"Not found {self.db_model.__name__} with email: {email}")
        except Exception as exc:
            await session.rollback()
            raise exc



    async def get_user_list(self, session: AsyncSession) -> list[UserList]:
        try:
            query = (
                select(self.db_model)
                .options(selectinload(self.db_model.accounts))
            )
            result = await session.execute(query)
            users = result.scalars().all()
        except Exception as error:
            raise error

        return [UserList(id=user.id, email=user.email, full_name=user.full_name, accounts=[Account(balance=account.balance) for account in user.accounts]) for user in users]

def get_user_repository() -> UserRepository:
    return UserRepository()
