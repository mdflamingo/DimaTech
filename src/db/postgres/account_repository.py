from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Account, User


class AccountRepository:
    db_model = Account
    db_user_model = User

    async def get_accounts(self, email: str, session: AsyncSession) -> list[Account]:
        try:
            query = (
                select(self.db_model)
                .join(self.db_user_model)
                .where(self.db_user_model.email == email)
            )
            result = await session.execute(query)
            accounts = result.scalars().all()
            return [Account(balance=account.balance) for account in accounts]
        except Exception as error:
            await session.rollback()
            raise error

def get_account_repository() -> AccountRepository:
    return AccountRepository()
