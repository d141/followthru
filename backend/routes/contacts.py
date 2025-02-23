from sqlalchemy.orm import joinedload
from models import Contact, Group
from middleware.auth import require_auth
from db import SessionLocal

import falcon

class HelloResource:
    def on_get(self, req, resp):
        resp.media = {"message": "Hello, world!"}

class ContactsResource:
    @require_auth
    def on_get(self, req, resp, user):
        """Handle GET requests to list all contacts"""
        user = req.context.get("user")  # Get authenticated user

        if not user:
            raise falcon.HTTPUnauthorized(description="Authentication required")
        
        with SessionLocal() as session:
            contacts = (
            session.query(Contact)
            .outerjoin(Group)  # Join groups table
            .options(joinedload(Contact.group))  # Optimize SQL query
            .filter(Contact.user_id == user.id)
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

class CreateContactResource:
    @require_auth
    def on_post(self, req, resp, user):
        """Create a new contact for the logged-in user"""
        data = req.media

        with SessionLocal() as session:
            contact = Contact(
                name=data["name"],
                email=data["email"],
                phone=data.get("phone"),
                group_id=data.get("group_id"),
                next_contact_date=data.get("next_contact_date"),
                user_id=user.id  # Associate contact with user
            )
            session.add(contact)
            session.commit()

        resp.status = falcon.HTTP_201
        resp.media = {"message": "Contact created", "contact": contact.to_dict()}
