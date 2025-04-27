from fastapi import APIRouter

from .user import router as user_router
from .admin import router as admin_router

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
