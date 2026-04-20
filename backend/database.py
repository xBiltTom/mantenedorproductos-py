"""
database.py - Configuración de conexión a PostgreSQL con SQLAlchemy
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# URL de conexión a PostgreSQL
# Puede configurarse via variable de entorno o usando valores por defecto
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123456@localhost:5432/product_manager"
)

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,          # Verifica conexiones antes de usarlas
    pool_size=10,                # Número de conexiones en el pool
    max_overflow=20,             # Conexiones adicionales permitidas
    echo=False                   # True para ver SQL en consola (debug)
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos.
    Uso en FastAPI como dependencia (Depends).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
