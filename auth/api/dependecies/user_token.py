from typing import Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import status, HTTPException
from jwt.exceptions import InvalidTokenError

from api.CRUD.user_crud import get_user_by_email, create_user

from api.routers.user_router import permission_check
from core.config import setting
from core.model import User, Role, RolesPermission, Permission
from core.schemas.user import UserCreate
from utils.jwt_validate import decode_jwt


def validate_type_token(
    token_type: str,
    payload: dict,
) -> bool:
    """
    Проверяем тип токена
    args:
        token_type: str - Тип(type) токена
        payload: dict - Словарь из расшифрованого токена
    return:
        bool — True, если тип токена валиден, иначе выбрасывает HTTPException
    """
    payload_type = payload.get(setting.auth_jwt.token_type_field)
    if payload_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type {payload_type!r} expected {token_type!r}",
    )


async def validate_payload(
    token: str,
) -> dict:
    """
    Деккодируем токен
    args:
        token: str - Токен
    return:
        payload: dict - Словарь расшифрованого токена
    """
    # Исключение в случае ошибки
    error_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Расшифровываем токен
        payload = decode_jwt(
            token=token,
            public_key=setting.auth_jwt.public_key_path.read_text(),
            algorithm=setting.auth_jwt.algorithm,
        )
        user_email = payload.get("sub")
        # Проверяем на наличие поля
        if not user_email:
            raise error_ex
    except InvalidTokenError:
        raise error_ex
    return payload


async def get_user_payload_syb(
    session: AsyncSession,
    token: str,
    token_type: str,
) -> Optional[Tuple[User, dict]]:
    """
    Получение access токена
    args:
        session: AsyncSession — сессия базы данных
        token: str — токен для проверки
        token_type: str - Тип(type) токена
    return:
        user_result, payload: Optional[Tuple[User, dict]] - Получаем пользователя и словарь расшифрованого токена
    """
    # Проверяем токен расшифровав
    payload = await validate_payload(token=token)
    user_email = payload.get("sub")
    # Проверяем на валидность типа токена
    validate_type_token(token_type=token_type, payload=payload)
    # Ищем пользователя в базе данных
    user_result = await get_user_by_email(session=session, email_user=user_email)
    if not user_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid {user_email} not found",
        )
    return user_result, payload


async def get_user_token(
    session: AsyncSession,
    token: str,
) -> Optional[Tuple[User, dict]]:
    """
    Получение access токена
    args:
        session: AsyncSession — сессия базы данных
        token: str — токен для проверки
    return:
        user_result, payload: user_result, payload: Optional[Tuple[User, dict]] - Получаем пользователя и словарь расшифрованого токена
    """
    access_type = setting.auth_jwt.access_token_type
    return await get_user_payload_syb(
        session=session,
        token=token,
        token_type=access_type,
    )


async def get_user_refresh_token(
    session: AsyncSession,
    token: str,
) -> Optional[Tuple[User, dict]]:
    """
    Получение refresh токена
    args:
        session: AsyncSession — сессия базы данных
        token: str — токен для проверки
    return:
        user_result, payload: Optional[Tuple[User, dict]] - Получаем пользователя и словарь расшифрованого токена
    """
    refresh_type = setting.auth_jwt.refresh_token_type
    return await get_user_payload_syb(
        session=session, token=token, token_type=refresh_type
    )


async def validation_user(
    session: AsyncSession,
    token: str,
    data_personal: UserCreate,
    role: str,
) -> User:
    payload = await validate_payload(token=token)
    user_email = payload.get("sub")

    # Проверяем на валидность role
    if role not in setting.roles.name_roles:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have specified an invalid role: {role}. You need to: {setting.roles.name_roles}",
        )

    # Ищем пользователя по почте из токена
    stmt = select(User).options(selectinload(User.role)).where(User.email == user_email)
    result_user = await session.scalars(stmt)
    user = result_user.first()
    # Проверяем у него роль
    await session.refresh(user)
    user_role_name = user.role.name
    if user_role_name not in setting.roles.personnel_recruitment_rights:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have specified an invalid role: {user_role_name}. You need to: {setting.roles.personnel_recruitment_rights}",
        )

    if role == "admin" and user_role_name != "admin":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You do not have sufficient rights to grant this role: {role}",
        )
    user = await create_user(
        session=session,
        data_user=data_personal,
        role_user=role,
    )
    return user


async def user_role(
    session: AsyncSession,
    token: str,
    product_code: str,
) -> bool:
    payload = await validate_payload(token=token)
    user_email = payload.get("sub")

    stmt = (
        select(User)
        .options(selectinload(User.role).selectinload(Role.permissions_helper))
        .where(User.email == user_email)
    )

    result_user = await session.scalars(stmt)
    user = result_user.first()
    if not user or not user.role:
        raise HTTPException(status_code=404, detail="User or role not found")

    permissions_codes = {p.code for p in user.role.permissions_helper}
    if product_code not in permissions_codes:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid, no permission",
        )
    return True
