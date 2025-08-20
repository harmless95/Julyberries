from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, TIMESTAMP, Text

from core.model import Base
from core.model.mixins.id_int_primary_key import IdIntPrKey


class Order(Base, IdIntPrKey):
    user_id: Mapped[int] = mapped_column()
    total_price: Mapped[DECIMAL] = mapped_column()
    cart_price: Mapped[DECIMAL] = mapped_column()
    delivery_price: Mapped[DECIMAL] = mapped_column()
    status: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
