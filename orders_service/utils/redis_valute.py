import redis
import logging

from core.config import setting

log = logging.getLogger(__name__)

redis_connect_check = redis.from_url(
    url=setting.redis_order.url,
    encoding="utf-8",
    decode_responses=True,
)


def main_redis(code_valute: str):
    try:
        if redis_connect_check.ping():
            log.info("Redis is available")
            value = redis_connect_check.get(f"rate:{code_valute}")
            log.info("Value for 'rate:%s': %s", code_valute, value)
            return value
        else:
            log.info("Redis ping failed")
    except redis.exceptions.RedisError as e:
        log.warning("Redis connection error: %s", e)
