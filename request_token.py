import jwt
from flask import Request


class AuthenticateToken:

    def __init__(self, request: Request):
        self.token = request.headers.get('token')

    def authenticate(self):
        try:
            return jwt.decode(self.token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise RuntimeError("Token expired")
        except jwt.InvalidTokenError:
            raise NameError("Token invalid")
