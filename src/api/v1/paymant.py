from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.connection import get_session
from src.models.paymant import Paymant
from src.services.paymant_service import PaymentService, get_payment_service

router = APIRouter()


@router.post(
    "/payment",
    status_code=status.HTTP_200_OK,
)
async def paymant(
    payment: Paymant,
    session: AsyncSession = Depends(get_session),
    payment_service: PaymentService = Depends(get_payment_service),
):
    try:
        return await payment_service.payment_process(payment=payment, session=session)
    except Exception as exc:
        logger.error(f"msg=Payment process error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{exc}"
        ) from exc
