import json
import logging
from aiokafka import AIOKafkaConsumer

logger = logging.getLogger(__name__)


async def consume():
    consumer = AIOKafkaConsumer(
        "ORDER_CREATED",
        bootstrap_servers="kafka1:9092",
        group_id="order-app",
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for message in consumer:
            logger.warning("Received message: %s", message)
    finally:
        await consumer.stop()
