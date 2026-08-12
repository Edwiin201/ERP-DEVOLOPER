"""
Configuracion del aplicativo.
Carga variables de entorno con validacion Pydantic.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuracion global del backend."""

    # Base de datos
    DATABASE_URL: str = "postgresql+psycopg://postgres:12345@localhost:5432/erp_manufactura"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Entorno
    APP_ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "ERP_"


@lru_cache()
def get_settings() -> Settings:
    """Retorna configuracion cacheada (singleton)."""
    return Settings()
