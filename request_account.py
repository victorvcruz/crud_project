from datetime import datetime

from flask import Request
from account import Account
from database import postgresql
from exception_error import CpfError, EmailError, PhoneError, CnpjError, DateError
import re

from validate_docbr import CPF, CNPJ
import phonenumbers


class RequestCreateAccount:

    def __init__(self, request: Request):
        input_json = request.get_json(force=True)

        self.login = input_json['login']
        self.password = input_json['password']

        cpf = input_json['cpf']
        if self.validate_cpf(cpf):
            self.cpf = cpf
        else:
            raise CpfError("invalid cpf")

        email = input_json['email']

        if self.validate_email(email):
            self.email = email
        else:
            raise EmailError("invalid email")

        phone = input_json['phone']
        if self.validate_phone(phone):
            self.phone = phone
        else:
            raise PhoneError("invalid phone number")

        cnpj = input_json['cnpj']
        if self.validate_cnpj(cnpj):
            self.cnpj = cnpj
        else:
            raise CnpjError("invalid cnpj")

        date = input_json['date']
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format")

        if self.validate_date(date):
            self.date = date
        else:
            raise DateError("invalid date")


    def insert_account(self, account: Account):
        postgresql.insert_account(account)

    def update_account_by_id(self, account: Account, id):
        postgresql.update_account_by_id(account, id)

    def validate_cpf(self, cpf):
        if len(cpf) == 11:
            validate = CPF()
            return validate.validate(cpf)

    def validate_email(self, email):
        regex = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        return re.search(regex, email)

    def validate_phone(self, phone):
        my_number = phonenumbers.parse(f"{phone}", "BR")
        return phonenumbers.is_valid_number(my_number)

    def validate_cnpj(self, cnpj):
        if len(cnpj) == 14:
            validatte_cnpj = CNPJ()
            return validatte_cnpj.validate(cnpj)

    def validate_date(self, date):
        if datetime.strptime(date, '%Y-%m-%d') < datetime.utcnow():
            regex = '([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
            return re.search(regex, date)
        else:
            return False
