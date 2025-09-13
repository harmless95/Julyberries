from celery import Celery
from celery.schedules import crontab

from core.config import setting
from httpx_api.httpx_data import valute_data
from redis_conf.redis_save_rate import save_redis

app = Celery("celery_app", broker=setting.redis_conf.url)

app.conf.beat_schedule = {
    "run": {"task": "celery_app.rate_valute", "schedule": crontab(minute="*/1")}
}


@app.task()
def rate_valute():
    result_valute = valute_data()
    result = save_redis(data_valute=result_valute)
