from fastapi import APIRouter
import fastapi

from core.config import setting
from core.schemas.user import UserRead, UserCreate
from .fastapi_users_router import fastapi_users_router, authentication_backend


router = APIRouter(
    prefix=setting.api.v1.auth,
    tags=["Auth"],
)

# login
# logout
router.include_router(
    router=fastapi_users_router.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)
# register
router.include_router(
    router=fastapi_users_router.get_register_router(
        UserRead,
        UserCreate,
    )
)
# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users_router.get_verify_router(UserRead),
)

# /forgot-password
# /reset-password

router.include_router(
    router=fastapi_users_router.get_reset_password_router(),
)
