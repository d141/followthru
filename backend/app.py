import falcon
from db import init_db
from middleware.auth import AuthMiddleware

app = falcon.App(middleware=[AuthMiddleware()])

# Initialize database at startup
init_db()


class CORSComponent:
    def process_request(self, req, resp):
        """Handles preflight CORS requests."""
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        resp.set_header("Access-Control-Allow-Headers", "Content-Type")

        # If this is a preflight request, respond with 200 and return immediately
        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            return


app = falcon.App(
    middleware=[
        CORSComponent(),  # Apply CORS middleware
        AuthMiddleware(),  # Apply authentication middleware
    ]
)

from routes.contacts import HelloResource, ContactsResource
from routes.auth import ChangePasswordResource, LoginResource, MeResource, SignupResource

app.add_route("/auth/change-password", ChangePasswordResource())
app.add_route("/auth/login", LoginResource())
app.add_route("/auth/me", MeResource())
app.add_route("/auth/signup", SignupResource())

app.add_route("/hello", HelloResource())
app.add_route("/contacts", ContactsResource())
