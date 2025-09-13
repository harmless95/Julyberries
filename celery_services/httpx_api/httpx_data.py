import httpx
import logging
from core.config import setting
from fastapi import HTTPException, status

log = logging.getLogger(__name__)


def valute_data():
    response = httpx.get(setting.valute_conf.url)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid valute data",
        )
    valute_data_api = response.json()
    log.warning("Полученные данные валют: %s", valute_data_api)
    return valute_data_api
