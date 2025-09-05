import asyncio
import json

from aiokafka import AIOKafkaConsumer


async def consume():
    consumer = AIOKafkaConsumer(
        "PRODUCT_UPDATED",
        bootstrap_servers="localhost:9092",
        group_id="my-group",
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for message in consumer:
            print("Received message:", message.value)
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
