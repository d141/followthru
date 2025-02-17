import falcon
from db import init_db

# Initialize database at startup
init_db()

class CORSComponent:
    def process_request(self, req, resp):
        """Handles preflight CORS requests."""
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        resp.set_header("Access-Control-Allow-Headers", "Content-Type")
        
        # If this is a preflight request, respond with 200 and return immediately
        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            return

# Apply CORS middleware
app = falcon.App(middleware=[CORSComponent()])

from routes.contacts import HelloResource, ContactsResource
app.add_route('/hello', HelloResource())
app.add_route('/contacts', ContactsResource())
