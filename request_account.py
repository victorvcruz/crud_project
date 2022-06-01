from datetime import datetime
from flask import Request

from exception_error import CpfError, EmailError, DateError, CnpjError, PhoneError, LoginError, PasswordError, DateFormatError, ConflictError, LoginShortSizeError, LoginLargeSizeError, PasswordLargeSizeError, PasswordShortSizeError
import re

from validate_docbr import CPF, CNPJ
import phonenumbers


class RequestCreateAccount:

    def __init__(self, request: Request):
        input_json = request.get_json(force=True)

        login = input_json['login']
        if len(login) > 18:
            raise LoginLargeSizeError("login exceeds 18 characters")
        if len(login) < 6:
            raise LoginShortSizeError("login too short")
        if self.validate_login(login):
            self.login = login
        else:
            raise LoginError("invalid login")

        password = input_json['password']
        if len(password) > 18:
            raise PasswordLargeSizeError("password exceeds 16 characters")
        if len(password) < 4:
            raise PasswordShortSizeError("password too short")
        if self.validate_password(password):
            self.password = password
        else:
            raise PasswordError("invalid password")

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
            raise DateFormatError("Incorrect date format")

        if self.validate_date(date):
            self.date = date
        else:
            raise DateError("invalid date")

    def validate_login(self, login):
        regex = "^[a-zA-Z0-9]+$"
        return re.search(regex, login)

    def validate_password(self, password):
        regex = "^[a-zA-Z0-9]+$"
        return re.search(regex, password)

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
