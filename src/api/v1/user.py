from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.connection import get_session
from src.db.postgres.user_repository import UserRepository, get_user_repository
from src.models.user import AuthenticatedUser
from src.services.user_service import UserService, get_user_service

router = APIRouter()


@router.post(
    "/auth",
    status_code=status.HTTP_200_OK,
    description="User authorization",
)
async def auth(
    user: AuthenticatedUser,
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
):
    try:
        if await user_service.auth(user=user, session=session):
            return "Successfully authorization"
        return "Auth failed"
    except Exception as exc:
        logger.error(f"msg=User authorization error: {exc}")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="user not found"
        ) from exc

# @router.post(
#     "/auth",
#     status_code=status.HTTP_200_OK,
#     description="User authorization",
# )
# async def get(
#     user: AuthenticatedUser,
#     session: AsyncSession = Depends(get_session),
#     user_repository: UserRepository = Depends(get_user_repository),
# ):
#     try:
#         return await user_repository.get_by_email(user=user, session=session)

#     except Exception as exc:
#         logger.error(f"msg=Get info error: {exc}")
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail="user not found"
#         ) from exc
