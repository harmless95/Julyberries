from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.model import User, Role
from core.schemas.user import UserCreate
from utils.jwt_validate import hash_password, validate_password


async def get_user_by_email(
    session: AsyncSession,
    email_user: str,
) -> User:
    """
    Ищем пользователя по электроной почте
    args:
        session: AsyncSession — сессия базы данных
        email_user: str - электроная почта
    return:
        user: User - Возвращаем модель User
    """
    stmt = select(User).where(User.email == email_user)
    result = await session.scalars(stmt)
    user = result.first()
    return user


async def create_user(
    session: AsyncSession,
    data_user: UserCreate,
) -> User:
    """
    Создаем user
    args:
        session: AsyncSession — сессия базы данных
        data_user: UserCreate - Данные нового пользователя
    return:
        user: User - Возвращаем модель User
    """
    # Ищем пользователя в базе данных на наличие
    user = await get_user_by_email(session=session, email_user=str(data_user.email))
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid there is already a user with this: {data_user.email}",
        )
    # Хэшируем пароль
    hash_bytes = hash_password(data_user.password)
    # Преобразуем пароль из байтов в строку для хранения в базе данных
    hex_hash = hash_bytes.hex()

    stmt_role = select(Role).where(Role.name == "user")
    result_role = await session.scalars(stmt_role)
    role = result_role.first()
    # if not role:
    #     role = Role(
    #         name=data_user.role.name,
    #         description=data_user.role.description,
    #     )
    #     session.add(role)
    #     await session.commit()
    #     await session.refresh(role)

    # Создаем пользователя
    user = User(
        email=data_user.email,
        hashed_password=hex_hash,
        name=data_user.name,
        role_id=role.id,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user, attribute_names=["role"])
    return user


async def auth_user(
    data_user: OAuth2PasswordRequestForm,
    session: AsyncSession,
) -> User:
    """
    Проверяем user
    args:
        data_user: OAuth2PasswordRequestForm - Получаем user из формы
        session: AsyncSession — сессия базы данных
    return:
        user: User - Возвращаем модель User
    """
    error_ex = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found or invalid credentials",
    )
    # Ищем пользователя в базе данных
    user = await get_user_by_email(session=session, email_user=str(data_user.username))
    if not user:
        raise error_ex
    # Сравниваем пароль
    user_password = validate_password(
        password=data_user.password,
        hashed_password=user.hashed_password,
    )
    if not user_password:
        raise error_ex
    return user
