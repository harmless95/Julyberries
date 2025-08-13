from typing import TYPE_CHECKING, Annotated
from fastapi import Depends

from core.auntefication.user_manager import UserManager
from .users import get_user_db

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    user_db: Annotated["SQLAlchemyUserDatabase", Depends(get_user_db)],
):
    yield UserManager(user_db=user_db)
