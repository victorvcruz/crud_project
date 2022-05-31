import datetime
import jwt
from flask import Flask, jsonify, request
from account import Account
from database import ConnectionPostgreSQL

app = Flask(__name__)
postgresql = ConnectionPostgreSQL()


@app.route('/accounts', methods=['POST'])
def create():
    input_json = request.get_json(force=True)

    login = input_json['login']
    password = input_json['password']
    cpf = input_json['cpf']
    email = input_json['email']
    phone = input_json['phone']
    cnpj = input_json['cnpj']
    date = input_json['date']

    account = Account(password, login, cpf,
                      email, phone, cnpj, date)

    postgresql.insert_account(account)

    return jsonify(account.json())


@app.route('/accounts/login', methods=['POST'])
def login():
    args = request.args

    login = args.get('login')
    password = request.headers.get('password')

    if not postgresql.authenticate_account(login, password):
        return jsonify({"message": "Password or login incorrect"}), 403

    id = postgresql.find_account_id_by_login(login)
    dt = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    encode = jwt.encode({
        'id': "{}".format(id),
        'exp': dt
    }, 'secret', algorithm='HS256')

    return jsonify({"token": "{}".format(encode)})


@app.route('/accounts', methods=['GET'])
def find():
    token = request.headers.get('token')

    try:
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid Token"}), 403

    find_account = postgresql.find_account_by_id(decode_token['id'])
    print(find_account)

    account = Account(find_account[2], find_account[1], find_account[3],
                      find_account[4], find_account[5], find_account[6], str(find_account[7]).replace(" 00:00:00", ""))

    return jsonify(account.json())


@app.route('/accounts', methods=['PUT'])
def change():
    input_json = request.get_json(force=True)

    token = request.headers.get('token')

    try:
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid Token"}), 403

    login = input_json['login']
    password = input_json['password']
    cpf = input_json['cpf']
    email = input_json['email']
    phone = input_json['phone']
    cnpj = input_json['cnpj']
    date = input_json['date']

    account = Account(password, login, cpf,
                      email, phone, cnpj, date)

    postgresql.update_account_by_id(account, decode_token['id'])

    return jsonify(account.json())


@app.route('/accounts', methods=['DELETE'])
def delete():
    token = request.headers.get('token')

    try:
        decode_token = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid Token"}), 403

    postgresql.delete_account_id_by_id(decode_token['id'])

    return jsonify({"message": "Deleted"}), 404
