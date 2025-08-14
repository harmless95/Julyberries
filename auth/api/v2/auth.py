from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from core.model import helper_db
from core.schemas.user import UserCreate, UserSchema
from .crud.user import create_user
from .dependencies.helper_jwt import create_access_token, create_refresh_token
from .dependencies.validates import validate_auth_user, get_current_token_payload

router = APIRouter(prefix="/auth", tags=["Auth"])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


@router.post("/register")
async def register_user(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_user: UserCreate,
):
    return await create_user(
        session=session,
        data_user=data_user,
    )


@router.post("/login")
async def login_user(
    user: Annotated[UserSchema, Depends(validate_auth_user)],
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me/")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
