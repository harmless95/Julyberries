from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Text
from fastapi import HTTPException, status

from core.model import Base
from core.model.mixins.id_int_primary_key import IdPrKey
from core.config import setting

if TYPE_CHECKING:
    from .user import User
    from .roles_permissions import RolesPermission


class Role(IdPrKey, Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship("User", back_populates="role")
    permissions_helper: Mapped[list["RolesPermission"]] = relationship(
        back_populates="role_r"
    )

    @validates("name")
    def validates_name(cls, key, name_role):
        if name_role not in setting.roles.name_roles:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Invalid name role: {name_role!r}, valid {setting.roles.name_roles!r}",
            )
        return name_role
