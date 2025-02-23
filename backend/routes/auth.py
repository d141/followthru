import datetime
import jwt
import falcon
import bcrypt
from models import User
from db import SessionLocal

class SignupResource:
    def on_post(self, req, resp):
        """Handles user registration (Sign Up)"""
        data = req.media

        # Validate input
        if not data.get("email") or not data.get("password") or not data.get("name"):
            resp.status = falcon.HTTP_400
            resp.media = {"error": "Missing required fields: email, password, name"}
            return

        email = data["email"].strip().lower()
        password = data["password"]
        name = data["name"].strip()

        with SessionLocal() as session:
            # Check if email is already in use
            if session.query(User).filter(User.email == email).first():
                resp.status = falcon.HTTP_400
                resp.media = {"error": "Email already in use"}
                return

            # Hash password
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

            # Create new user
            new_user = User(email=email, password_hash=password_hash, name=name)
            session.add(new_user)
            session.commit()

            resp.status = falcon.HTTP_201
            resp.media = {"message": "User registered successfully"}

# Secret key for signing JWTs (keep this safe!)
#TODO
SECRET_KEY = "your_super_secret_key"

class LoginResource:
    def on_post(self, req, resp):
        """Handles user login and JWT token generation"""
        data = req.media

        # Validate input
        if not data.get("email") or not data.get("password"):
            resp.status = falcon.HTTP_400
            resp.media = {"error": "Missing email or password"}
            return

        email = data["email"].strip().lower()
        password = data["password"]

        with SessionLocal() as session:
            # Find user in database
            user = session.query(User).filter(User.email == email).first()

            if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
                resp.status = falcon.HTTP_401
                resp.media = {"error": "Invalid email or password"}
                return

            # Generate JWT token
            token_payload = {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)  # Token expires in 7 days
            }
            token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

            resp.status = falcon.HTTP_200
            resp.media = {
                "message": "Login successful",
                "token": token
            }

class MeResource:
    """Handles user profile & settings"""

    def on_get(self, req, resp):
        """Return the authenticated user's profile"""
        user = req.context.get("user")  # Get authenticated user

        if not user:
            raise falcon.HTTPUnauthorized(description="Authentication required")

        resp.media = user.to_dict()  # Return user info

    def on_put(self, req, resp):
        """Allow users to update their settings"""
        user = req.context.get("user")

        if not user:
            raise falcon.HTTPUnauthorized(description="Authentication required")

        data = req.media

        with SessionLocal() as session:
            db_user = session.query(User).filter(User.id == user.id).first()
            if not db_user:
                raise falcon.HTTPUnauthorized(description="User not found")

            # Update user settings (merge new data with existing JSON)
            if "settings" in data:
                db_user.settings.update(data["settings"])

            session.commit()

            resp.status = falcon.HTTP_200
            resp.media = {"message": "Profile updated successfully", "user": db_user.to_dict()}

class ChangePasswordResource:
    """Handles password changes"""

    def on_put(self, req, resp):
        """Allow users to update their password"""
        user = req.context.get("user")  # Get authenticated user

        if not user:
            raise falcon.HTTPUnauthorized(description="Authentication required")

        data = req.media

        # Validate input
        if not data.get("old_password") or not data.get("new_password"):
            resp.status = falcon.HTTP_400
            resp.media = {"error": "Missing old_password or new_password"}
            return

        old_password = data["old_password"]
        new_password = data["new_password"]

        # Verify old password
        if not bcrypt.checkpw(old_password.encode(), user.password_hash.encode()):
            resp.status = falcon.HTTP_401
            resp.media = {"error": "Old password is incorrect"}
            return

        # Hash new password
        new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

        # Update password in database
        with SessionLocal() as session:
            db_user = session.query(User).filter(User.id == user.id).first()
            if not db_user:
                raise falcon.HTTPUnauthorized(description="User not found")

            db_user.password_hash = new_password_hash
            session.commit()

            resp.status = falcon.HTTP_200
            resp.media = {"message": "Password updated successfully"}
