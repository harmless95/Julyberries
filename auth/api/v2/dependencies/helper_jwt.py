from datetime import timedelta

from utils import jwt_validate as auth_utils
from core.config import setting
from core.schemas.user import UserSchema


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = setting.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {setting.auth_jwt.token_type_field: token_type}
    jwt_payload.update(token_data)
    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {
        # subject
        "sub": user.email,
        "username": user.name,
        "email": user.email,
        # "logged_in_at"
    }
    return create_jwt(
        token_type=setting.auth_jwt.access_token_type,
        token_data=jwt_payload,
        expire_minutes=setting.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {
        "sub": user.email,
        # "username": user.name,
    }
    return create_jwt(
        token_type=setting.auth_jwt.refresh_token_type,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=setting.auth_jwt.refresh_token_expire_days),
    )
