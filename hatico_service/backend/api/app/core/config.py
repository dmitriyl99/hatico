from typing import List, Union, Optional

from pydantic import BaseSettings, AnyHttpUrl, validator, HttpUrl

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: Optional[str] = "/api/v1"
    PROJECT_NAME: str

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SENTRY_DSN: Optional[HttpUrl] = None

    MONGO_DB_HOST: str
    MONGO_DB_NAME: str


settings = Settings()

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'app.core.logging.json_logger.JSONLogFormatter',
        },
    },
    'handlers': {
        # Используем AsyncLogDispatcher для асинхронного вывода потока.
        'json': {
            'formatter': 'json',
            'class': 'asynclog.AsyncLogDispatcher',
            'func': 'app.core.logging.json_logger.write_log',
        },
    },
    'loggers': {
        'test_project': {
            'handlers': ['json'],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn': {
            'handlers': ['json'],
            'level': 'INFO',
            'propagate': False,
        },
        # Не даем стандартному логгеру fastapi работать по пустякам и замедлять работу сервиса
        'uvicorn.access': {
            'handlers': ['json'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
