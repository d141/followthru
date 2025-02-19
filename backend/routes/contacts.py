from sqlalchemy.orm import joinedload
from models import Contact, Group
from db import SessionLocal

class HelloResource:
    def on_get(self, req, resp):
        resp.media = {"message": "Hello, world!"}

class ContactsResource:
    def on_get(self, req, resp):
        """Handle GET requests to list all contacts"""
        with SessionLocal() as session:
            contacts = (
            session.query(Contact)
            .outerjoin(Group)  # Join groups table
            .options(joinedload(Contact.group))  # Optimize SQL query
            .all()
        )
            
        resp.media = [
            {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "group": contact.group.name if contact.group else "No group",
                "next_contact_date": contact.next_contact_date.isoformat() if contact.next_contact_date else None,
            }
            for contact in contacts
        ]
