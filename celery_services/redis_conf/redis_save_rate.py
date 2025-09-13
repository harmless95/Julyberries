from core.config import setting
from redis_conf.redis_connect import redis_connect
from utils.validate_curs import formate_save


def save_redis(data_valute):
    base_rate = formate_save(data_valute=data_valute)
    if base_rate is None:
        raise ValueError("Base currency rate not found")

    for valute in data_valute["ValCurs"]["Valute"]:
        char_code = valute.get("CharCode")
        value_str = valute.get("Value").replace(",", ".")
        nominal = valute.get("Nominal", 1)
        rate = float(value_str) / nominal
        rate_to_base = round(rate / base_rate, 5)  # курс валюты относительно базового
        redis_connect.set(
            f"rate:{char_code}", rate_to_base, ex=setting.redis_conf.expire_second
        )
