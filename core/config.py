from typing import List, ClassVar
from pytz import timezone
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_URL: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://user_notaconforme:nota789463@localhost:5432/notaconforme'
    V_TIME_ZONE: ClassVar = 'America/Sao_Paulo'
    DBBaseModel: ClassVar = declarative_base()

    JWT_SECRET: str = 'kcOMPV3RhB-9nMTQbbRvNtyewBRAsnPJbZ3JE0-Va7g'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43200

    class Config:
        case_sensitive = True

settings: Settings = Settings()
