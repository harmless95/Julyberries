from decimal import Decimal
from uuid import UUID
import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status, Request

from api.Dependencies.service_httpx import is_cast_present_all

from core.config import setting
from core.model import Order, OrderItem
from core.schemas.schema_orders import OrderCreate
from utils.redis_valute import main_redis

log = logging.getLogger(__name__)


async def get_product_dict(products_all: list) -> dict:
    # Создаём словарь для быстрого поиска продукта по имени
    return {item["name"]: item for item in products_all}


async def get_currency_rate(currency: str) -> Decimal:
    # Предполагаю, что main_redis может быть асинхронной функцией
    # Здесь добавьте обработку ошибок и возврат дефолтного курса
    try:
        rate = await main_redis(currency)
        return Decimal(rate)
    except Exception as e:
        # Логирование ошибки или fallback
        return Decimal("1.0")  # Если не удалось получить курс, вернуть 1


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
    products_all = await is_cast_present_all(
        url_service=setting.product.url, request=request
    )
    product_dict = await get_product_dict(products_all)
    grocery_basket = {}
    for product in data_order.products_name:
        count_product = product.count
        product_name = product.name
        product_res = product_dict.get(product_name)
        if not product_res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invalid product: {product_name} not found",
            )
        price = Decimal(product_res["price"])
        grocery_basket[product_name] = price * count_product

    cart_price_sum = sum(grocery_basket.values())
    amount_currency = cart_price_sum

    if data_order.currency:
        rate_currency = await get_currency_rate(data_order.currency)
        amount_currency = (cart_price_sum * rate_currency).quantize(Decimal("0.01"))
    total_price = amount_currency + Decimal(data_order.delivery_price)

    order = Order(
        user_id=request.state.user["id"],
        total_price=total_price,
        cart_price=amount_currency,
        delivery_price=Decimal(data_order.delivery_price),
        status=data_order.status,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    for product in data_order.products_name:
        product_res = product_dict.get(product.name)
        if not product_res:
            continue

        order_item = OrderItem(
            order_id=order.id,
            product_id=product_res["id"],
            quantity=product.count,
            unit_price=Decimal(product_res["price"]),
        )
        session.add(order_item)

    await session.commit()

    return order
