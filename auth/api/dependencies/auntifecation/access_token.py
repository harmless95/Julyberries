from typing import Annotated, TYPE_CHECKING
from fastapi import Depends

from core.model import helper_db, AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(helper_db.session_getter)],
):
    yield AccessToken.get_db(session=session)
