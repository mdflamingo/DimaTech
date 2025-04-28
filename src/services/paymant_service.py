import hashlib
from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.db.postgres.account_repository import AccountRepository, get_account_repository
from src.db.postgres.paymant_repository import PaymentRepository, get_paymant_repository
from src.db.postgres.user_repository import UserRepository, get_user_repository
from src.models.paymant import Paymant


@dataclass
class PaymentService:
    user_repository: UserRepository
    account_repository: AccountRepository
    payment_repository: PaymentRepository

    def _generate_hmac_signature(self, data: dict):
        payload = {
            "account_id": str(data.get("account_id")),
            "amount": str(data.get("amount")),
            "transaction_id": data.get("transaction_id"),
            "user_id": str(data.get("user_id")),
        }

        sorted_keys = sorted(payload.keys())

        message = "".join(payload[key] for key in sorted_keys)
        message += settings.secret_key

        expected_signature = hashlib.sha256(message.encode()).hexdigest()
        return expected_signature

    async def payment_process(self, payment: Paymant, session: AsyncSession):

        if payment.signature != self._generate_hmac_signature(payment.model_dump()):
            raise ValueError("Invalid signature")
        try:
            await self.payment_repository.get_or_create(
                payment=payment, session=session
            )
            await self.account_repository.get_or_create(
                payment_data=payment, session=session
            )
        except Exception as error:
            await session.rollback()
            raise error


def get_payment_service(
    user_repository: UserRepository = Depends(get_user_repository),
    account_repository: AccountRepository = Depends(get_account_repository),
    payment_repository: PaymentRepository = Depends(get_paymant_repository),
) -> PaymentService:
    return PaymentService(
        user_repository=user_repository,
        account_repository=account_repository,
        payment_repository=payment_repository,
    )
