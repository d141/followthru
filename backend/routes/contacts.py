from models import Contact
from db import SessionLocal

class HelloResource:
    def on_get(self, req, resp):
        resp.media = {"message": "Hello, world!"}

class ContactsResource:
    def on_get(self, req, resp):
        """Handle GET requests to list all contacts"""
        with SessionLocal() as session:
            contacts = session.query(Contact).all()
        resp.media = {"contacts": [contact.to_dict() for contact in contacts]}


