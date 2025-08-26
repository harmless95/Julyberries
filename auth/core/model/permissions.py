from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String

from core.model import Base
from core.model.mixins.id_int_primary_key import IdPrKey


if TYPE_CHECKING:
    from .roles_permissions import RolesPermission


class Permission(IdPrKey, Base):
    code: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(Text)

    roles_helper: Mapped[list["RolesPermission"]] = relationship(
        back_populates="permission_r",
    )
