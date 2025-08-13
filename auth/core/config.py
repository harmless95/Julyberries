from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel


class PrefixV1(BaseModel):
    prefix: str = "/v1"


class PrefixConfig(BaseModel):
    prefix: str = "/api"
    v1: PrefixV1 = PrefixV1()


class Run(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DataBaseConfig
    run: Run = Run()
    prefix: PrefixConfig = PrefixConfig()


setting = Setting()
