from aiokafka import AIOKafkaProducer

from core.schema.reviews_schema import ReviewsRead


async def validate_price_decimal(review_data: ReviewsRead, producer: AIOKafkaProducer):
    message_json = review_data.model_dump_json()
    message_bytes = message_json.encode("utf-8")
    await producer.send_and_wait("REVIEW_CREATED", message_bytes)
