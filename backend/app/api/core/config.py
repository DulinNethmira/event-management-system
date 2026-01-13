import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Event Management System"

    DATABASE_URL: str
    
    VONAGE_API_KEY: str
    VONAGE_API_SECRET: str
    VONAGE_FROM_NUMBER: str = "InfinityEvents"

    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587

    REMINDER_DAYS_AHEAD: int = 3
    REMINDER_TIME_HOUR: int = 9

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()