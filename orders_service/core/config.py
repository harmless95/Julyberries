from typing import Literal
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel

# fmt: off
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# fmt: on
BASE_DIR = Path(__file__).resolve().parent.parent


class ServiceProduct(BaseModel):
    url: str = "http://catalogs_services:8000/products/"


class PrefixConfig(BaseModel):
    prefix: str = "/orders"
    tags: str = "Order"


class Run(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debag",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class RedisConfig(BaseModel):
    url: str = "redis://:redis_p@redis:6379/0"


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DataBaseConfig
    redis_order: RedisConfig = RedisConfig()
    run: Run = Run()
    api: PrefixConfig = PrefixConfig()
    log: LoggingConfig = LoggingConfig()
    product: ServiceProduct = ServiceProduct()


setting = Setting()
