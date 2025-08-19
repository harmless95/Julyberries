from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DECIMAL, Numeric, ForeignKey, TIMESTAMP

from core.model import Base

from core.model.mixins.id_int_primary_key import IdIntPrKey

if TYPE_CHECKING:
    from core.model import Category


class Product(Base, IdIntPrKey):
    name: Mapped[str] = mapped_column(String(150), unique=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[DECIMAL] = mapped_column(Numeric(10, 2))
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")
