import os
from typing import ClassVar

from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
    Configuracoes gerais usadas na aplicaco
    """
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://doadmin:AVNS_uvj4yNFuuialz5-c_ju@db-cs-do-user-2961515-0.c.db.ondigitalocean.com:25060/geobee"
    DBBaseModel: ClassVar = declarative_base()


    JWT_SECRET: str = 'HoGF2ucrNRiAH7VmxQ3Lo-08Dk2P8OITMNVDL9CWDio'
    """
    import secrets
    token = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = "HS256"
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()