from aiokafka import AIOKafkaProducer

from core.models.reviews import Reviews


async def validate_price_decimal(review_data: Reviews, producer: AIOKafkaProducer):
    message_json = review_data.model_dump_json()
    message_bytes = message_json.encode("utf-8")
    await producer.send_and_wait("REVIEW_CREATED", message_bytes)
