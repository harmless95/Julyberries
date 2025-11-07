import asyncio
import logging

from celery import Celery
from celery.schedules import crontab

from core.config import setting
from httpx_api.httpx_data import valute_data
from redis_conf.redis_save_rate import save_redis
from api.Dependencies.kafka_consumer import consume

app = Celery("celery_app", broker=setting.redis_conf.url)
logger = logging.getLogger(__name__)

app.conf.beat_schedule = {
    "run": {
        "task": "celery_app.rate_valute",
        "schedule": setting.redis_conf.expire_second,
    }
}

app.conf.beat_schedule = {
    "run": {
        "task": "celery_app.order_create",
        "schedule": setting.redis_conf.expire_second,
    }
}


@app.task()
def rate_valute():
    result_valute = valute_data()
    result = save_redis(data_valute=result_valute)


@app.task()
def order_create():
    asyncio.run(consume())
