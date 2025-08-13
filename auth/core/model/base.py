from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData

from core.config import setting
from utils import conv_file


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=setting.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{conv_file(cls.__name__)}s"
