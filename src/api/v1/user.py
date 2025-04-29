from fastapi import APIRouter, Depends, HTTPException, Query, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres.account_repository import AccountRepository, get_account_repository
from db.postgres.amount_repository import AmountRepository, get_amount_repository

from db.postgres.connection import get_session
from db.postgres.user_repository import UserRepository, get_user_repository
from models.account import Account
from models.user import AuthenticatedUser, UserInDB
from services.user_service import UserService, get_user_service

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
) -> str:
    try:
        authenticated_user = await user_service.auth(user=user, session=session)
        if not authenticated_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        return authenticated_user.email
    except Exception as exc:
        logger.error(f"msg=User authorization error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{exc}"
        ) from exc


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    description="User info",
)
async def get_info(
    email: str = Query(),
    session: AsyncSession = Depends(get_session),
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserInDB | None:
    try:
        user = await user_repository.get_by_email(email=email, session=session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User  not found"
            )
        return UserInDB(**user.__dict__)

    except Exception as exc:
        logger.error(f"msg=Get info error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{exc}"
        ) from exc


@router.get(
    "/account/list",
    status_code=status.HTTP_200_OK,
    description="Get account list",
    response_model=list[Account],
)
async def get_account_list(
    email: str = Query(),
    session: AsyncSession = Depends(get_session),
    account_repository: AccountRepository = Depends(get_account_repository),
) -> list[Account]:
    try:
        return await account_repository.get_accounts(email=email, session=session)

    except Exception as exc:
        logger.error(f"msg=Get accounts error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{exc}"
        ) from exc


@router.get(
    "/amount/list",
    status_code=status.HTTP_200_OK,
    description="Get amount list",
)
async def get_amount_list(
    email: str = Query(),
    session: AsyncSession = Depends(get_session),
    amount_repository: AmountRepository = Depends(get_amount_repository),
):
    try:
        return await amount_repository.get_amounts(email=email, session=session)

    except Exception as exc:
        logger.error(f"msg=Get amounts error: {exc}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{exc}"
        ) from exc
