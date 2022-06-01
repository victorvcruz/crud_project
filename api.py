from flask import Flask, jsonify, request
from account import Account
from database import postgresql
from request_account import RequestCreateAccount
from exception_error import CpfError, EmailError, DateError, CnpjError, PhoneError, LoginError, PasswordError, \
    DateFormatError, LoginShortSizeError, LoginLargeSizeError, PasswordLargeSizeError, \
    PasswordShortSizeError
from request_login import RequestLogin
from request_token import AuthenticateToken

app = Flask(__name__)


@app.route('/accounts', methods=['POST'])
def create():
    try:
        request_account = RequestCreateAccount(request)

        account = Account(request_account.password, request_account.login, request_account.cpf,
                          request_account.email, request_account.phone,
                          request_account.cnpj, request_account.date)

        if postgresql.exists_account_by_login(request_account.login):
            return jsonify({"message": "login already used"}), 409

        postgresql.insert_account(account)

        return jsonify(account.json())

    except LoginLargeSizeError:
        return jsonify({"message": "login exceeds 18 characters"}), 400
    except LoginShortSizeError:
        return jsonify({"message": "short login"}), 400
    except LoginError:
        return jsonify({"message": "login invalid"}), 400
    except PasswordError:
        return jsonify({"message": "password invalid"}), 400
    except PasswordLargeSizeError:
        return jsonify({"message": "password exceeds 16 characters"}), 400
    except PasswordShortSizeError:
        return jsonify({"message": "short password"}), 400
    except CpfError:
        return jsonify({"message": "cpf invalid"}), 400
    except EmailError:
        return jsonify({"message": "email invalid"}), 400
    except PhoneError:
        return jsonify({"message": "phone number invalid"}), 400
    except CnpjError:
        return jsonify({"message": "cnpj invalid"}), 400
    except DateFormatError:
        return jsonify({"message": "incorrect date format"}), 400
    except DateError:
        return jsonify({"message": "date invalid"}), 400


@app.route('/accounts/login', methods=['POST'])
def login():
    request_login = RequestLogin(request)

    if not postgresql.authenticate_account(request_login.login, request_login.password):
        return jsonify({"message": "Password or login incorrect"}), 403

    id = postgresql.find_account_by_login(request_login.login)

    return jsonify({"token": "{}".format(request_login.encode(id))})


@app.route('/accounts', methods=['GET'])
def find():
    token_request = AuthenticateToken(request)

    try:
        decode_token = token_request.authenticate()

        if not postgresql.exists_account_by_id(decode_token['id']):
            return jsonify({"message": "Unauthorized Token"}), 403

        account = postgresql.find_account_by_id(decode_token['id'])
        return jsonify(account.json())
    except RuntimeError:
        return jsonify({"message": "Token expired"}), 403
    except NameError:
        return jsonify({"message": "Invalid Token"}), 403


@app.route('/accounts', methods=['PUT'])
def change():
    token_request = AuthenticateToken(request)

    try:
        decode_token = token_request.authenticate()

        if not postgresql.exists_account_by_id(decode_token['id']):
            return jsonify({"message": "Unauthorized Token"}), 403

        request_account = RequestCreateAccount(request)

        account = Account(request_account.password, request_account.login, request_account.cpf,
                          request_account.email, request_account.phone,
                          request_account.cnpj, request_account.date)

        postgresql.update_account_by_id(account, decode_token['id'])

        return jsonify(account.json())

    except RuntimeError:
        return jsonify({"message": "Token expired"}), 403
    except NameError:
        return jsonify({"message": "Invalid Token"}), 403
    except LoginLargeSizeError:
        return jsonify({"message": "login exceeds 18 characters"}), 400
    except LoginShortSizeError:
        return jsonify({"message": "short login"}), 400
    except LoginError:
        return jsonify({"message": "login invalid"}), 400
    except PasswordError:
        return jsonify({"message": "password invalid"}), 400
    except PasswordLargeSizeError:
        return jsonify({"message": "password exceeds 16 characters"}), 400
    except PasswordShortSizeError:
        return jsonify({"message": "short password"}), 400
    except CpfError:
        return jsonify({"message": "cpf invalid"}), 400
    except EmailError:
        return jsonify({"message": "email invalid"}), 400
    except PhoneError:
        return jsonify({"message": "phone number invalid"}), 400
    except CnpjError:
        return jsonify({"message": "cnpj invalid"}), 400
    except DateFormatError:
        return jsonify({"message": "incorrect date format"}), 400
    except DateError:
        return jsonify({"message": "date invalid"}), 400


@app.route('/accounts', methods=['DELETE'])
def delete():
    token_request = AuthenticateToken(request)

    try:
        decode_token = token_request.authenticate()

        if not postgresql.exists_account_by_id(decode_token['id']):
            return jsonify({"message": "Unauthorized Token"}), 403

    except RuntimeError:
        return jsonify({"message": "Token expired"}), 403
    except NameError:
        return jsonify({"message": "Invalid Token"}), 403

    postgresql.delete_account_id_by_id(decode_token['id'])

    return jsonify({"message": "Successfully deleted"})
