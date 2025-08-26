from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.user_crud import create_user, auth_user
from api.dependecies.helpers import create_access_token, create_refresh_token
from api.dependecies.user_token import get_user_token, get_user_refresh_token
from core.config import setting
from core.model import helper_db, AccessToken
from core.schemas.token import TokenBase
from core.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix=setting.api.prefix,
    tags=[setting.api.tags],
    dependencies=[Depends(setting.auth_jwt.http_bearer)],
)


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
    access_token, logged_in_at = create_access_token(user=user)
    token_save = AccessToken(
        user_id=user.id,
        token=access_token,
        created_at=logged_in_at,
    )
    session.add(token_save)
    await session.commit()
    await session.refresh(token_save)
    refresh_token = create_refresh_token(user=user)
    return TokenBase(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me/")
async def user_me(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    payload: str = Depends(setting.auth_jwt.oauth2_scheme),
):
    user, payload_user = await get_user_token(session=session, token=payload)
    logged_in_at = payload_user.get("logged_in_at")
    return {
        "email": user.email,
        "name": user.name,
        "logged_in_at": logged_in_at,
    }


@router.post(
    "/refresh/",
    response_model=TokenBase,
    response_model_exclude_none=True,
)
async def refresh_jwt_token(
    session: Annotated[AsyncSession, Depends(helper_db.session_getter)],
    data_user: str = Depends(setting.auth_jwt.oauth2_scheme),
):
    user, payload = await get_user_refresh_token(session=session, token=data_user)
    access_token, logged_in_at = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenBase(
        access_token=access_token,
        refresh_token=refresh_token,
    )
