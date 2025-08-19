from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from catalogs_services.core.model import Product


async def get_all(
    session: AsyncSession,
) -> Sequence[Product]:
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    products = result.all()
    return products


async def get_product_id(
    session: AsyncSession,
    product_id: int,
):
    stmt = select(Product).where(Product.id == product_id)
    result = await session.scalars(stmt)
    product = result.first()
    return product
