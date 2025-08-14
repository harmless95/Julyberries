from typing import Annotated
from fastapi import Form, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v2.crud.user import get_user_by_email
from core.config import setting
from core.model import helper_db
from core.schemas.user import UserSchema
from utils.jwt_validate import validate_password
from utils import jwt_validate as auth_utils

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-auth/jwt/login/",
)


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(setting.auth_jwt.token_type_field)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
    session: Annotated[AsyncSession, Depends(helper_db)], payload: dict
) -> UserSchema:
    email: str | None = payload.get("sub")
    user = await get_user_by_email(session=session, email_user=email)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    def get_auth_user_from_token(
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return get_user_by_token_sub(payload)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_of_type(
    setting.auth_jwt.access_token_type
)


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )


async def validate_auth_user(
    session: Annotated[AsyncSession, Depends(helper_db)],
    email: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = await get_user_by_email(session=session, email_user=email)
    if not user:
        raise unauthed_exc

    if not validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exc

    return user
