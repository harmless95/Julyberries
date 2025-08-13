from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, BaseModel

# fmt: off
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# fmt: on


class PrefixV1(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"
    messages: str = "/messages"


class PrefixConfig(BaseModel):
    prefix: str = "/api"
    v1: PrefixV1 = PrefixV1()

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


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


class AccessTokenConfig(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debag",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class ConfigRedis(BaseSettings):
    url: str = "redis://localhost"
    password: str = "password"
    user: str = "user"
    user_password: str = "password"


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DataBaseConfig
    access_token: AccessTokenConfig
    run: Run = Run()
    api: PrefixConfig = PrefixConfig()
    log: LoggingConfig = LoggingConfig()
    redis: ConfigRedis = ConfigRedis()


setting = Setting()
