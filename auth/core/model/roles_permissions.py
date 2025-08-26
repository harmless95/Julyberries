from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

from core.model import Base
from core.model.mixins.id_int_primary_key import IdPrKey

if TYPE_CHECKING:
    from .roles import Role
    from .permissions import Permission


class RolesPermission(IdPrKey, Base):
    __tablename__ = "roles_permissions"
    __table_args__ = (
        UniqueConstraint(
            "roles_id",
            "permission_id",
            name="idx_role_permissions",
        ),
    )

    roles_id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("roles.id")
    )
    permission_id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("permissions.id")
    )

    role_r: Mapped["Role"] = relationship(back_populates="permissions_helper")
    permission_r: Mapped["Permission"] = relationship(back_populates="roles_helper")
