from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DOUBLE_PRECISION, UniqueConstraint

from core.model import Base
from core.model.mixins.id_int_primary_key import IdIntPrKey

if TYPE_CHECKING:
    from .orders import Order


class OrderItem(Base, IdIntPrKey):
    __table_args__ = UniqueConstraint(
        "order_id",
        "product_id",
        name="idx_uniq_order_product",
    )
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(DOUBLE_PRECISION)

    order: Mapped["Order"] = relationship("Order", back_populates="product_item")
