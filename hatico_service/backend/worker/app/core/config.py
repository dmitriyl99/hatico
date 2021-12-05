from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    MONGO_DB_HOST: str
    MONGO_DB_NAME: str

    DATA_DIR: str


settings = Settings()
