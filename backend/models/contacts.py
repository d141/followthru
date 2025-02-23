from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("Group", back_populates="contacts")  # Relationship to Group
    next_contact_date = Column(DateTime, default=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="contacts")  # Relationship to User

    def to_dict(self):
        """Convert model instance to dictionary for JSON responses"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "group_id": self.group_id,
            "group": self.group.name if self.group else "No group",
            "next_contact_date": self.next_contact_date.isoformat() if self.next_contact_date else None,
            "user_id": self.user_id,  # Include user ID in response
        }

