from datetime import datetime, timedelta

import jwt
from flask import Request



class RequestLogin:

    def __init__(self, request: Request):
        args = request.args

        self.login = args.get('login')
        self.password = request.headers.get('password')

    def encode(self, id):
        encode = jwt.encode({
            'id': "{}".format(id),
            'exp': datetime.utcnow() + timedelta(minutes=5)
        }, 'secret', algorithm='HS256')

        return encode
