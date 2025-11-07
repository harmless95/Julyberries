import json

from aiokafka import AIOKafkaProducer

from core.model import Order


async def order_producer(data_order: Order, producer: AIOKafkaProducer, topic: str):
    data_json = json.dumps(data_order)
    data_encode = data_json.encode("utf-8")
    await producer.send_and_wait(topic, data_encode)
