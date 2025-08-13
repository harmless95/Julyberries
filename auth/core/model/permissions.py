from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String

from core.model import Base
from core.model.mixins.id_int_primary_key import IdIntPrKey
from .roles_permissions import roles_permissions_table

if TYPE_CHECKING:
    from .roles import Role


class Permission(Base, IdIntPrKey):
    code: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(Text)

    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=roles_permissions_table,
        back_populates="permissions",
    )
