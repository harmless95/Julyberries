from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from api.Dependencies.service_httpx import is_cast_present_all

from core.config import setting
from core.model import Order
from core.schemas.schema_orders import OrderCreate


async def get_order(session: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await session.scalars(stmt)
    order = result.first()
    return order


async def create_order(
    session: AsyncSession,
    data_order: OrderCreate,
) -> Order:

    grocery_basket = {}
    products_all = await is_cast_present_all(url_service=setting.product.url)
    products = data_order.products_name
    for product_name in products:
        product_res = next(
            (item for item in products_all if item.get("name") == product_name), None
        )
        if not product_res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid product: {product_name} not found",
            )
        grocery_basket[product_res["name"]] = Decimal(product_res["price"])
    cart_price_sum = sum(grocery_basket.values())
    total_price = cart_price_sum + data_order.delivery_price
    order = Order(
        user_id=data_order.user_id,
        total_price=total_price,
        cart_price=cart_price_sum,
        delivery_price=data_order.delivery_price,
        status=data_order.status,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order
