from datetime import timedelta

from core.config import setting

redis = None


async def init_redis(redis_url: str):
    global redis
    import aioredis

    redis = aioredis.from_url(redis_url)


async def close_redis():
    global redis
    if redis:
        await redis.close()


# Добавляем текущий access токен в blacklist на время его жизни или на фиксированный срок
async def blacklist_token(token: str):
    await redis.set(
        f"blacklist:{token}",
        "true",
        ex=timedelta(days=setting.auth_jwt.blacklist_token_expire_days),
    )


async def is_blacklisted(token: str):
    exists = await redis.get(f"blacklist:{token}")
    return exists is not None


# Проверяем есть ли такой refresh token в Redis (валидность)
async def get_stored_refresh_token(username: str):
    token = await redis.get(f"refresh:{username}")
    if token:
        return token.decode()
    return None


# Создаем refresh token и сохраняем его в Redis
async def store_refresh_token(username: str, refresh_token: str):
    await redis.set(
        f"refresh:{username}",
        refresh_token,
        ex=timedelta(days=setting.auth_jwt.refresh_token_expire_days),
    )
