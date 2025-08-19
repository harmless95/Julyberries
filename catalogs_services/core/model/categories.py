from typing import TYPE_CHECKING
from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP

from core.model import Base
from core.model.mixins.id_int_primary_key import IdIntPrKey

if TYPE_CHECKING:
    from catalogs_services.core.model import Product


class Category(Base, IdIntPrKey):
    name: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )
