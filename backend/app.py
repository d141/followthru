import falcon
from db import init_db
from middleware.auth import AuthMiddleware
from middleware.cors import CORSComponent

# Initialize database at startup
init_db()


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
