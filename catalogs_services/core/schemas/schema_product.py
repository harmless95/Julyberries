from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


from core.schemas.schema_category import CategoryCreate, CategoryRead


class ProductCreate(BaseModel):
    name: str
    description: str
    price: Decimal
    category: Optional["CategoryCreate"]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    category: Optional["CategoryRead"]

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
