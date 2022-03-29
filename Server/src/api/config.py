import logging
import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.getenv("DATABASE_URL")
    ip_api_key: str = os.getenv("IP_API_KEY")
    secret: str = os.getenv("SECRET")
    algorithm: str = os.getenv("ALGO")


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
