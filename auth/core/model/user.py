from datetime import datetime, timezone
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP

from core.model import Base
from .mixins.id_int_primary_key import IdPrKey


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .roles import Role


class User(IdPrKey, Base):
    email: Mapped[str] = mapped_column(
        String(length=320),
        unique=True,
        index=True,
        nullable=False,
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    name: Mapped[str] = mapped_column(String)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    role: Mapped["Role"] = relationship("Role", back_populates="users")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
