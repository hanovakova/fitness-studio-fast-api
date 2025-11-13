import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.orm_models.base import Base

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost") # 'localhost' is correct if app runs on host
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "FitnessStudio")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    """Creates all tables in the database."""
    print(f"Connecting to database at {DB_HOST}:{DB_PORT} to create tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully (if they didn't already exist).")
    except Exception as e:
        print(f"Error creating tables: {e}")

def get_db():
    """
    FastAPI dependency to get a database session.
    Ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()