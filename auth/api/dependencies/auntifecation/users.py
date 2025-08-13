from typing import TYPE_CHECKING, Annotated
from fastapi import Depends

from core.model import helper_db, User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(
    session: Annotated["AsyncSession", Depends(helper_db.session_getter)],
):
    yield User.get_db(session=session)
