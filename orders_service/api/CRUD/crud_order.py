from decimal import Decimal
from uuid import UUID
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Request

from api.Dependencies.service_httpx import is_cast_present_all

from core.config import setting
from core.model import Order
from core.schemas.schema_orders import OrderCreate
from utils.redis_valute import main_redis

log = logging.getLogger(__name__)


async def get_order(session: AsyncSession, order_id: UUID) -> Order:
    stmt = select(Order).where(Order.id == order_id)
    result = await session.scalars(stmt)
    order = result.first()
    return order


async def create_order(
    request: Request,
    session: AsyncSession,
    data_order: OrderCreate,
) -> Order:

    grocery_basket = {}
    products_all = await is_cast_present_all(
        url_service=setting.product.url, request=request
    )
    products = (
        data_order.products_name
    )  # [{"name": "яблоко", "count": 1}, {"name": "яблоко", "count": 4}]
    for product in products:
        count_product = product.count
        product_name = product.name
        product_res = next(
            (item for item in products_all if item.get("name") == product_name), None
        )
        if not product_res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid product: {product_name} not found",
            )
        grocery_basket[product_res["name"]] = (
            Decimal(product_res["price"]) * count_product
        )
    cart_price_sum = sum(grocery_basket.values())
    amount_currency = cart_price_sum
    if data_order.currency:
        rate_currency = main_redis(data_order.currency)
        amount_currency = float(cart_price_sum) * float(rate_currency)
    total_price = amount_currency + data_order.delivery_price
    order = Order(
        user_id=request.state.user["id"],
        total_price=total_price,
        cart_price=amount_currency,
        delivery_price=data_order.delivery_price,
        status=data_order.status,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order
