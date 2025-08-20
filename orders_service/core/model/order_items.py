import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, ForeignKey, DOUBLE_PRECISION

from core.model import Base
from core.model.mixins.id_int_primary_key import IdIntPrKey


class OrderItem(Base, IdIntPrKey):
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("orders.id")
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id")
    )
    quantity: Mapped[int] = mapped_column()
    unit_price: Mapped[float] = mapped_column(DOUBLE_PRECISION)
