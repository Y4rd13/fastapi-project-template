import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import ClassVar, List

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Template API"
    PROJECT_VERSION: str = "1.0.0"  # (major.minor.patch)
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND")

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    MONGO_URI: str = os.getenv("MONGO_URI")

    class Config:
        env_file = ".env" # change to doppler or aws secrets manager

settings = Settings()