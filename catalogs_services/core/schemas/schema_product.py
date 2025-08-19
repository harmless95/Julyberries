from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import DECIMAL

from catalogs_services.core.schemas.schema_category import CategoryCreate, CategoryRead


class ProductCreate(BaseModel):
    name: str
    description: str
    price: DECIMAL
    category: Optional["CategoryCreate"]

    model_config = ConfigDict(from_attributes=True)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: DECIMAL
    category: Optional["CategoryRead"]

    model_config = ConfigDict(from_attributes=True)
