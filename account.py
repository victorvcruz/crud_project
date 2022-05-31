import uuid


class Account:

    def __init__(self, password, login, cpf, email, phone, cnpj, date):
        self.id = str(uuid.uuid4())
        self.password = password
        self.login = login
        self.cpf = cpf
        self.email = email
        self.phone = phone
        self.cnpj = cnpj
        self.date = date

    def json(self):
        json = {
            'login': self.login,
            'password': self.password,
            'cpf': self.cpf,
            'email': self.email,
            'phone': self.phone,
            'cnpj': self.cnpj,
            'date': self.date
        }
        return json
