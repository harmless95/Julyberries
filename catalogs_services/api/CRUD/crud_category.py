from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.model import Category


async def all_categories(
    session: AsyncSession,
) -> Sequence[Category]:
    stmt = select(Category).order_by(Category.id)
    result = await session.scalars(stmt)
    categories = result.all()
    return categories
