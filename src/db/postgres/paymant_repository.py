from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from models.paymant import Paymant as payment_request

from db.postgres.models import Payment


class PaymentRepository:
    db_model = Payment

    async def get_or_create(self, payment: payment_request, session: AsyncSession):
        try:
            query = select(self.db_model).where(
                self.db_model.transaction_id == payment.transaction_id
            )
            result = await session.execute(query)
            existing_payment = result.scalar_one_or_none()

            if existing_payment:
                raise ValueError("Transaction already processed")

            create_query = insert(self.db_model).values(
                {
                    "amount": payment.amount,
                    "account_id": payment.account_id,
                    "transaction_id": payment.transaction_id,
                }
            )
            await session.execute(create_query)
            await session.commit()
        except Exception as error:
            await session.rollback()
            raise error


def get_paymant_repository() -> PaymentRepository:
    return PaymentRepository()
