from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from core.model import User
from core.schemas.user import UserCreate, UserToken
from utils.jwt_validate import hash_password


async def get_user_by_email(
    session: AsyncSession,
    email_user: str,
):
    stmt = select(User).where(User.email == email_user)
    result = await session.scalars(stmt)
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid not found",
        )
    return user


async def create_user(
    session: AsyncSession,
    data_user: UserCreate,
) -> User:
    user_data = data_user.model_dump()
    user_data["hashed_password"] = hash_password(user_data.pop("password", None))
    user = User(**user_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user(session: AsyncSession, data_user: UserToken):
    pass
