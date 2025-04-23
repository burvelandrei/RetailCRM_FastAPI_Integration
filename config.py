from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    RETAILCRM_SUBDOMAIN: str
    RETAILCRM_API_KEY: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
