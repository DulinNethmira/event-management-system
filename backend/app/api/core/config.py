from pydantic import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432"

    class Config:
        env_file = ".env"

settings = Settings()
