from flask import Flask, jsonify, request
from account import Account
from database import postgresql
from exception_error import CpfError, EmailError, DateError, CnpjError, PhoneError
from request_account import RequestCreateAccount
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

        request_account.insert_account(account)
    except CpfError:
        return jsonify({"message": "cpf invalid"}), 400
    except EmailError:
        return jsonify({"message": "email invalid"}), 400
    except PhoneError:
        return jsonify({"message": "phone number invalid"}), 400
    except CnpjError:
        return jsonify({"message": "cnpj invalid"}), 400
    except ValueError:
        return jsonify({"message": "incorrect date format"}), 400
    except DateError:
        return jsonify({"message": "date invalid"}), 400

    return jsonify(account.json())


@app.route('/accounts/login', methods=['POST'])
def login():
    request_login = RequestLogin(request)

    try:
        request_login.authenticate_account()
    except AttributeError:
        return jsonify({"message": "Password or login incorrect"}), 403

    return jsonify({"token": "{}".format(request_login.encode())})


@app.route('/accounts', methods=['GET'])
def find():
    token_request = AuthenticateToken(request)

    try:
        decode_token = token_request.authenticate()
    except RuntimeError:
        return jsonify({"message": "Token expired"}), 403
    except NameError:
        return jsonify({"message": "Invalid Token"}), 403

    find_account = postgresql.find_account_by_id(decode_token['id'])
    print(find_account)

    account = Account(find_account[2], find_account[1], find_account[3],
                      find_account[4], find_account[5], find_account[6], str(find_account[7]).replace(" 00:00:00", ""))

    return jsonify(account.json())


@app.route('/accounts', methods=['PUT'])
def change():
    token_request = AuthenticateToken(request)
    request_account = RequestCreateAccount(request)

    try:
        decode_token = token_request.authenticate()
    except RuntimeError:
        return jsonify({"message": "Token expired"}), 403
    except NameError:
        return jsonify({"message": "Invalid Token"}), 403

    account = Account(request_account.password, request_account.login, request_account.cpf,
                      request_account.email, request_account.phone,
                      request_account.cnpj, request_account.date)

    request_account.update_account_by_id(account, decode_token['id'])

    return jsonify(account.json())


@app.route('/accounts', methods=['DELETE'])
def delete():
    token_request = AuthenticateToken(request)

    try:
        decode_token = token_request.authenticate()
    except RuntimeError:
        return jsonify({"message": "Token expired"}), 403
    except NameError:
        return jsonify({"message": "Invalid Token"}), 403

    postgresql.delete_account_id_by_id(decode_token['id'])

    return jsonify({"message": "Successfully deleted"})
