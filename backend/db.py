from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from models import User

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://followthru:secret@db:5432/followthru_db")

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True)  # Log SQL queries for debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    db = SessionLocal()
    try:
        default_user = db.query(User).filter_by(username="admin").first()
        if not default_user:
            default_user = User(username="admin")
            db.add(default_user)
            db.commit()
            print("Created default user: admin")
        else:
            print("Default user 'admin' already exists")
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()