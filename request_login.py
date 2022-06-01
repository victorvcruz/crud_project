from datetime import datetime, timedelta

import jwt
from flask import Request, jsonify

from database import postgresql


class RequestLogin:

    def __init__(self, request: Request):
        args = request.args

        self.login = args.get('login')
        self.password = request.headers.get('password')

    def authenticate_account(self):
        if postgresql.authenticate_account(self.login, self.password):
            pass
        else:
            raise AttributeError

    def encode(self):
        id = postgresql.find_account_id_by_login(self.login)

        encode = jwt.encode({
            'id': "{}".format(id),
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }, 'secret', algorithm='HS256')

        return encode
