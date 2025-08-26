from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTable,
    SQLAlchemyAccessTokenDatabase,
)
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

from core.model import Base
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIdType]):
    token: Mapped[str] = mapped_column(Text, primary_key=True)
    user_id: Mapped[UserIdType] = mapped_column(
        UUID_PG(as_uuid=True),
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, cls)
