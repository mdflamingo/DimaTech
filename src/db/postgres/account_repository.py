from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.paymant import Paymant

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

    async def get_or_create(self, payment_data: Paymant, session: AsyncSession) -> None:
        get_query = select(self.db_model).where(
            and_(
                self.db_model.id == payment_data.account_id,
                self.db_model.user_id == payment_data.user_id,
            )
        )
        result = await session.execute(get_query)
        account = result.scalar()
        if account:
            new_balance = account.balance + payment_data.amount
            update_query = (
                update(self.db_model)
                .where(self.db_model.id == account.id)
                .values(balance=new_balance)
            )
            await session.execute(update_query)
            await session.commit()

        else:
            user_query = select(self.db_user_model).where(
                self.db_user_model.id == payment_data.user_id
            )
            user_result = await session.execute(user_query)
            user = user_result.scalar_one_or_none()
            if not user:
                raise ValueError("User  not found")

            try:
                create_query = self.db_model(
                    user_id=payment_data.user_id, balance=payment_data.amount
                )
                await session.execute(create_query)
                await session.commit()
            except Exception as error:
                await session.rollback()
                raise error


def get_account_repository() -> AccountRepository:
    return AccountRepository()
