from typing import Literal
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

# fmt: off
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# fmt: on
BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigValute(BaseModel):
    url: str = "http://example_api_services:8000/valute/"
    valute: str = "USD"


class Run(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debag",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class ConfigRedis(BaseModel):
    url: str
    expire_second: int = 60


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
    redis_conf: ConfigRedis
    run: Run = Run()
    log: LoggingConfig = LoggingConfig()
    valute_conf: ConfigValute = ConfigValute()


setting = Setting()
