from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Text

from core.model import Base
from core.model.mixins.id_int_primary_key import IdIntPrKey
from core.config import setting
from .roles_permissions import roles_permissions_table

if TYPE_CHECKING:
    from .user import User
    from .permissions import Permission


class Role(Base, IdIntPrKey):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary=roles_permissions_table,
        back_populates="roles",
    )

    @validates("name")
    def validates_name(cls, key, name_role):
        if name_role not in setting.roles.name_roles:
            raise ValueError(f"Invalid name role: {name_role}")
        return name_role
