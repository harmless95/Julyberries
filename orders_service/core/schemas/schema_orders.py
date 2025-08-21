from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    user_id: int
    products_name: list[str]
    delivery_price: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    user_id: int
    total_price: Decimal
    cart_price: Decimal
    delivery_price: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
