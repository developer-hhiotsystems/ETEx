"""
ETEx - Database Configuration

SQLAlchemy database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

# Get project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Get database URL from environment or use default SQLite
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{PROJECT_ROOT}/data/database/etex.db"
)

# Ensure database directory exists
db_path = PROJECT_ROOT / "data" / "database"
db_path.mkdir(parents=True, exist_ok=True)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # Set to True to log SQL queries
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Import models for Alembic migrations
# This ensures Alembic can detect model changes
from models import (  # noqa: F401, E402
    AuthoritativeSource,
    Term,
    TermSynonym,
    Translation,
    UploadedDocument,
)

# Dependency for FastAPI routes
def get_db():
    """
    Database dependency for FastAPI routes.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
