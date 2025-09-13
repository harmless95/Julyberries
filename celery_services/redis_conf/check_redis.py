import redis

redis_connect_check = redis.from_url(
    url="redis://:redis_p@localhost:6380/0",
    encoding="utf-8",
    decode_responses=True,
)


def main_redis():
    try:
        if redis_connect_check.ping():
            print("Redis is available")
            value = redis_connect_check.get("rate:AUD")
            print(f"Value for 'rate:AUD': {value}")
        else:
            print("Redis ping failed")
    except redis.exceptions.RedisError as e:
        print(f"Redis connection error: {e}")


if __name__ == "__main__":
    main_redis()
