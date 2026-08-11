"""
Configuracion de base de datos con SQLAlchemy 2.0.
Crea el engine, session factory y base declarativa.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# Engine con soporte para PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

# Session factory para transacciones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base declarativa para modelos ORM
Base = declarative_base()


def get_db():
    """Dependency de FastAPI para obtener sesion de BD.
    Garantiza cierre de sesion al finalizar request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
