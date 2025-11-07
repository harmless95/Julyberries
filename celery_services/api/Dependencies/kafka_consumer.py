import json
from aiokafka import AIOKafkaConsumer


async def consume():
    consumer = AIOKafkaConsumer(
        "ORDER_CREATED",
        bootstrap_servers="localhost:9092",
        group_id="my-group",
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    await consumer.start()
    try:
        async for message in consumer:
            print("Received message:", message)
    finally:
        await consumer.stop()
