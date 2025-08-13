from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy

from core.config import setting
from .access_token import get_access_token_db

if TYPE_CHECKING:
    from core.model import AccessToken


def get_database_strategy(
    access_token_db: Annotated[
        AccessTokenDatabase["AccessToken"],
        Depends(
            get_access_token_db,
        ),
    ],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=setting.access_token.lifetime_seconds,
    )
