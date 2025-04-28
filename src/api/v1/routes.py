from fastapi import APIRouter

from src.api.v1.user import router as user_router
from src.api.v1.admin import router as admin_router
from src.api.v1.paymant import router as paymant_router

router = APIRouter(prefix="/api/v1")

router.include_router(
    user_router,
    prefix="/user",
    tags=["User"],
)

router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"],
)

router.include_router(
    paymant_router,
    prefix="/paymant",
    tags=["Paymant"],
)
