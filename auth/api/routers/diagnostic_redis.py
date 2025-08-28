from fastapi import APIRouter

from api.dependecies.redis_client import redis

router = APIRouter(tags=["Diagnostic"])


@router.get("/debug/redis/{key}")
async def get_redis_key(key: str):
    value = await redis.get(f"refresh:{key}")
    return {"key": key, "value": value}
