from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.user_crud import create_user
from core.model import helper_db, User
from core.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_user: UserCreate,
) -> UserRead:
    user = await create_user(
        session=session,
        data_user=data_user,
    )
    return UserRead.model_validate(user)
