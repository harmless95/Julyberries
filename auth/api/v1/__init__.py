from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import setting
from .auth import router as router_auth
from .user import router as router_users
from .messages import router as router_messages

http_bearer = HTTPBearer(auto_error=False)

router_v1 = APIRouter(
    prefix=setting.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router_v1.include_router(router=router_auth)
router_v1.include_router(router=router_users)
router_v1.include_router(router=router_messages)
