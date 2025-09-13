import redis

from core.config import setting

redis_connect = redis.from_url(
    url=setting.redis_conf.url,
    encoding="utf-8",
    decode_responses=True,
)
