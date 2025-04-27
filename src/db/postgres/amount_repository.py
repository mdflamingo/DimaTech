from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.user_repository import UserRepository, get_user_repository
from src.models.amount import Amount

from .models import Account, Payment, User


class AmountRepository:
    db_model = Payment
    db_user_model = User
    db_account_model = Account

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_amounts(self, email: str, session: AsyncSession):
        user = await self.user_repository.get_by_email(email=email, session=session)
        try:
            query = (
                select(self.db_model)
                .join(self.db_account_model)
                .where(self.db_account_model.user_id == user.id)
            )
            result = await session.execute(query)
            amounts = result.scalars().all()
            return [
                Amount(amount=amount.amount, account_id=amount.account_id)
                for amount in amounts
            ]
        except Exception as error:
            await session.rollback()
            raise error


def get_amount_repository(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AmountRepository:
    return AmountRepository(user_repository=user_repository)
