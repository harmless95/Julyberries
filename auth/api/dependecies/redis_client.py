from redis import asyncio as aioredis

from core.config import setting

redis = aioredis.from_url(
    setting.redis.url,
    encoding="utf-8",
    decode_responses=True,
)
