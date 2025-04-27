from fastapi import APIRouter, Depends, HTTPException, Query, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres.account_repository import (AccountRepository,
                                                get_account_repository)
from src.db.postgres.admin_repository import AdminRepository, get_admin_repository
from src.db.postgres.amount_repository import (AmountRepository,
                                               get_amount_repository)
from src.db.postgres.connection import get_session
from src.db.postgres.user_repository import UserRepository, get_user_repository
from src.models.account import Account
from src.models.user import AuthenticatedUser, UserInDB
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
    admin_repository: AdminRepository = Depends(get_admin_repository),
) -> str:
    try:
        authenticated_admin = await admin_repository.get_by_email(email=user.email, session=session)
        if not authenticated_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return authenticated_admin.email
    except Exception as exc:
        logger.error(f"msg=User authorization error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{exc}"
        ) from exc

@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    description="Admin info",
)
async def get_info(
    email: str = Query(),
    session: AsyncSession = Depends(get_session),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserInDB | None:
    try:
        user = await user_repository.get_by_email(email=email, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")
        return UserInDB(**user.__dict__)

    except Exception as exc:
        logger.error(f"msg=Get info error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{exc}"
        ) from exc
