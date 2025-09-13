from celery import Celery
import redis
from fastapi import Request

BASE_URL = "http://localhost:8000/valute"

app = Celery("celery_app", broker="redis://localhost:6379/0")
