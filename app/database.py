from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL (e.g., postgresql://user:password@localhost/dbname)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)

# SessionLocal class is an instance of sessionmaker
# It will be used to create database session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for your models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
