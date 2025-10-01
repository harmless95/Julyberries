from fastapi import Request
from aiokafka import AIOKafkaProducer


def get_producer(request: Request) -> AIOKafkaProducer:
    return request.app.state.producer
