from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contacts = relationship("Contact", back_populates="group")  # Define relationship

    def to_dict(self):
        """Convert model instance to dictionary for JSON responses"""
        return {
            "id": self.id,
            "name": self.name,
        }