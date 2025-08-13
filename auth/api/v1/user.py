from fastapi import APIRouter

from core.schemas.user import UserRead, UserUpdate
from .fastapi_users_router import fastapi_users_router
from core.config import setting

router = APIRouter(prefix=setting.api.v1.users, tags=["Users"])
# /me
# /{id}
router.include_router(
    router=fastapi_users_router.get_users_router(
        UserRead,
        UserUpdate,
    )
)
