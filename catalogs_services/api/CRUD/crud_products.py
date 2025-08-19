from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import HTTPException, status

from core.model import Product
from core.schemas.schema_product import ProductCreate
from core.model import Category


async def get_all(
    session: AsyncSession,
) -> Sequence[Product]:
    stmt = select(Product).options(selectinload(Product.category)).order_by(Product.id)
    result = await session.scalars(stmt)
    products = result.all()
    return products


async def get_product_id(
    session: AsyncSession,
    product_id: int,
):
    stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(Product.id == product_id)
    )
    result = await session.scalars(stmt)
    product = result.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: {product_id!r} not found",
        )
    return product


async def create_product(
    session: AsyncSession,
    data_product: ProductCreate,
) -> Product:
    category_name = data_product.category.name
    stmt_category = select(Category).where(Category.name == category_name)
    result = await session.scalars(stmt_category)
    category = result.first()
    if not category:
        category = Category(
            name=category_name,
        )
        session.add(category)
        await session.commit()
        await session.refresh(category)

    stmt_product = select(Product).where(Product.name == data_product.name)
    result = await session.scalars(stmt_product)
    product = result.first()
    if product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid {data_product.name!r} the product already exists",
        )
    product = Product(
        name=data_product.name,
        description=data_product.description,
        price=data_product.price,
        category=category,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product, attribute_names=["category"])
    return product
