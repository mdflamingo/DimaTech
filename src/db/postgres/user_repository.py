from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Account, User


class UserRepository:
    db_model = User
    db_account_model = Account

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

    async def get_accounts(self, email: str, session: AsyncSession) -> list[Account]:
        try:
            query = (
                select(self.db_account_model)
                .join(self.db_model)
                .where(self.db_model.email == email)
            )
            result = await session.execute(query)
            accounts = result.scalars().all()
            return [Account(balance=account.balance) for account in accounts]
        except Exception as error:
            await session.rollback()
            raise error

def get_user_repository() -> UserRepository:
    return UserRepository()
