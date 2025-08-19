from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.user_crud import create_user, auth_user
from api.dependecies.helpers import create_access_token, create_refresh_token
from core.model import helper_db, User
from core.schemas.token import TokenBase
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


@router.post(
    "/login",
    response_model=TokenBase,
    status_code=status.HTTP_200_OK,
)
async def get_login(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_user: OAuth2PasswordRequestForm = Depends(),
):
    user = await auth_user(session=session, data_user=data_user)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenBase(
        access_token=access_token,
        refresh_token=refresh_token,
    )
