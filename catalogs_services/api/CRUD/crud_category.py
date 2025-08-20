from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from core.model import Category


async def all_categories(
    session: AsyncSession,
) -> Sequence[Category]:
    stmt = select(Category).order_by(Category.id)
    result = await session.scalars(stmt)
    categories = result.all()
    return categories


async def get_category(
    session: AsyncSession,
    category_id: int,
) -> Category:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.scalars(stmt)
    category = result.first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: {category_id} not found",
        )
    return category
