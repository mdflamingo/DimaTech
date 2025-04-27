from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.connection import get_session

router = APIRouter()


@router.post(
    "/auth",
    status_code=status.HTTP_200_OK,
    description="User authorization",
)
async def auth(
session: AsyncSession = Depends(get_session)
):
    # try:
    #     await signup(user_create.model_dump(), session)
    # except Exception as exc:
    #     logger.error(f"msg=Error user registration: {exc}")
    #     raise HTTPException(
    #         status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="user not created"
    #     ) from exc
    return "ok"
