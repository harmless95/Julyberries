from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from .schema_order_item import OrderItemCreate


class OrderCreate(BaseModel):
    products_name: list[OrderItemCreate]
    delivery_price: int
    status: str
    currency: str = "USD"

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: UUID
    user_id: UUID
    total_price: Decimal
    cart_price: Decimal
    delivery_price: Decimal
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class OrderUpdate(BaseModel):
    user_id: UUID | None = None
    total_price: Decimal | None = None
    cart_price: Decimal | None = None
    delivery_price: Decimal | None = None
    status: str | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
