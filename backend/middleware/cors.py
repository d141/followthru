import falcon
from .auth import require_auth

class CORSComponent:
    def process_request(self, req, resp):
        """Handles preflight CORS requests."""
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS"
        )
        resp.set_header("Access-Control-Allow-Headers", "Authorization, Content-Type")

        # If this is a preflight request, respond with 200 and return immediately
        if req.method == "OPTIONS":
            resp.status = falcon.HTTP_200
            return