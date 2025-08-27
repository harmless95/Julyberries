from typing import TYPE_CHECKING
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DECIMAL, TIMESTAMP, Text, Numeric

from .base import Base
from .mixins.id_int_primary_key import IdPrKey

if TYPE_CHECKING:
    from .order_items import OrderItem


class Order(Base, IdPrKey):
    user_id: Mapped[UUID] = mapped_column()
    total_price: Mapped[DECIMAL] = mapped_column(Numeric(10, 2))
    cart_price: Mapped[DECIMAL] = mapped_column(Numeric(10, 2))
    delivery_price: Mapped[DECIMAL] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    product_item: Mapped[list["OrderItem"]] = relationship(back_populates="order")
