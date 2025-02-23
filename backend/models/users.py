from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    settings = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship to Contacts
    contacts = relationship("Contact", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model instance to dictionary for JSON responses"""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "settings": self.settings,
            "created_at": self.created_at.isoformat(),
        }
