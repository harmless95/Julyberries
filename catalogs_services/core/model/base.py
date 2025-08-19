from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData

from catalogs_services.core.config import setting
from catalogs_services.utils.conv_file import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=setting.db.naming_convention)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
