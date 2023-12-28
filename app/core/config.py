from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    DB_URL: str = os.getenv('DB_URL')
    BASE_URL: str = os.getenv('BASE_URL')


setting = Settings()
