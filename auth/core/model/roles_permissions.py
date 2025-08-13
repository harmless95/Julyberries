from sqlalchemy import Table, Column, ForeignKey, Integer

from core.model import Base

roles_permissions_table = Table(
    "roles_permissions_table",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)
