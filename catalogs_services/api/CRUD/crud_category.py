from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from core.model import Category
from core.schemas.schema_category import CategoryCreate, CategoryUpdate


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


async def create_category(
    session: AsyncSession,
    data_category: CategoryCreate,
) -> Category:
    stmt = select(Category).where(Category.name == data_category.name)
    result = await session.scalars(stmt)
    category = result.first()
    if category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid {data_category.name!r} the category already exists",
        )
    category = Category(
        name=data_category.name,
    )
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def update_category(
    session: AsyncSession,
    data_update: CategoryUpdate,
    category: Category,
    partial: bool = False,
) -> Category:
    for name, value in data_update.model_dump(exclude_unset=partial).items():
        setattr(category, name, value)
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category
