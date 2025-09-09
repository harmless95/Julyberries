from decimal import Decimal
import json
from aiokafka import AIOKafkaProducer

from core.model import Product
from core.schemas.schema_product import ProductUpdate


async def validate_price_decimal(
    data_update: ProductUpdate, product: Product, producer: AIOKafkaProducer
):
    if data_update.price is not None and float(data_update.price) != float(
        product.price
    ):
        data_product = {
            "name": product.name,
            "old_price": product.price,
            "new_price": data_update.price,
        }
        message_bytes = json.dumps(
            data_product,
            default=lambda v: float(v) if isinstance(v, Decimal) else v,
        ).encode("utf-8")
        await producer.send_and_wait("PRODUCT_UPDATED", message_bytes)
