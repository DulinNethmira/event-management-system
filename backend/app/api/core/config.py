import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Event Management System"

    DATABASE_URL: str
    
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_SMS_NUMBER: str

    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True
    )

settings = Settings()