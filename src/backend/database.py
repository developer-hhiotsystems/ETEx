"""
ETEx - Database Configuration

SQLAlchemy database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

# Get database URL from environment or use default SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/database/etex.db")

# Ensure database directory exists
db_path = Path("./data/database")
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
