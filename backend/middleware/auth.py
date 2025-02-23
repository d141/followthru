import falcon
import jwt
from functools import wraps
from db import SessionLocal
from models import User

SECRET_KEY = "your_super_secret_key"  # Must match auth.py

def require_auth(func):
    """Decorator to require authentication for Falcon resources"""
    @wraps(func)
    def wrapper(self, req, resp, *args, **kwargs):
        # Allow CORS preflight OPTIONS requests to pass through
        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            return

        auth_header = req.get_header("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise falcon.HTTPUnauthorized(
                title="Authentication Required",
                description="Missing or invalid authorization token",
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                raise falcon.HTTPUnauthorized(title="Invalid Token", description="Invalid token payload")

            # Fetch user from database
            with SessionLocal() as session:
                user = session.query(User).filter_by(id=user_id).first()

                if not user:
                    raise falcon.HTTPUnauthorized(title="Invalid User", description="User not found")

            kwargs["user"] = user  # Attach user to request
            return func(self, req, resp, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            raise falcon.HTTPUnauthorized(title="Token Expired", description="Please log in again")

        except jwt.InvalidTokenError:
            raise falcon.HTTPUnauthorized(title="Invalid Token", description="Token is not valid")

    return wrapper


class AuthMiddleware:
    """Middleware to enforce JWT authentication for protected routes"""

    def process_request(self, req, resp):
        """Run before handling a request"""
        # Skip authentication for public routes
        if req.path in ["/auth/login", "/auth/signup"] or req.method == "OPTIONS":
            return

        auth_header = req.get_header("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise falcon.HTTPUnauthorized(description="Missing or invalid token")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")

            if not user_id:
                raise falcon.HTTPUnauthorized(description="Invalid token")

            # Attach user to request context
            with SessionLocal() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    raise falcon.HTTPUnauthorized(description="User not found")

                req.context["user"] = user  # Store user in request context

        except jwt.ExpiredSignatureError:
            raise falcon.HTTPUnauthorized(description="Token has expired")
        except jwt.InvalidTokenError:
            raise falcon.HTTPUnauthorized(description="Invalid token")
