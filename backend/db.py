from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import Base, Contact, Group  # Ensure both models are imported

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://followthru:secret@db:5432/followthru_db")

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)  # Log SQL queries for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
def init_db():
    from models.base import Base
    Base.metadata.create_all(bind=engine)
