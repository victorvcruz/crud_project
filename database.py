import psycopg2

from account import Account



class ConnectionPostgreSQL:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="postgres",
            port="5432")

        print("Database connected")

    def insert_account(self, account: Account):
        try:
            cur = self.conn.cursor()

            sql = """
                INSERT INTO public.account(id, login, password, cpf, email, phone, cnpj, date) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """

            cur.execute(sql,
                        (account.id, account.login, account.password, account.cpf, account.email, account.phone,
                         account.cnpj, account.date))

            self.conn.commit()
            cur.close()

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert into table", error)

    def authenticate_account(self, login, password):
        try:
            cur = self.conn.cursor()

            sql = """
                    SELECT
                    FROM public.account
                    WHERE password = %s
                    AND login = %s
            """

            cur.execute(sql,
                        (password, login))
            records = cur.fetchall()
            cur.close()

            if records:
                return True
            else:
                return False

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert into table", error)

    def find_account_by_login(self, login):
        try:
            cur = self.conn.cursor()

            sql = """
                    SELECT id
                    FROM public.account
                    WHERE login = %s
            """

            cur.execute(sql,
                        (login,))
            records = cur.fetchall()
            cur.close()

            if records:
                return records[0][0]

        except (Exception, psycopg2.Error) as error:
            print("Failed to insert into table", error)

    def find_account_by_id(self, id):
        try:
            cur = self.conn.cursor()

            sql = """
                    SELECT id, login, password, cpf, email, phone, cnpj, date
                    FROM public.account
                    WHERE id = %s
            """

            cur.execute(sql,
                        (id,))
            records = cur.fetchall()
            cur.close()

            if records:
                account = Account(records[0][2], records[0][1], records[0][3],
                                  records[0][4], records[0][5], records[0][6],
                                  str(records[0][7]).replace(" 00:00:00", ""))
                return account


        except (Exception, psycopg2.Error) as error:
            print("Failed to insert into table", error)


    def update_account_by_id(self, account: Account, id):
        try:
            cur = self.conn.cursor()

            sql = """
                    UPDATE public.account
                    SET login = %s, password = %s, cpf = %s, email = %s, phone = %s, cnpj = %s, date = %s
                    WHERE id = %s
            """

            cur.execute(sql,
                        (account.login, account.password, account.cpf, account.email, account.phone, account.cnpj, account.date, id))

            self.conn.commit()
            cur.close()


        except (Exception, psycopg2.Error) as error:
            print("Failed to insert into table", error)

    def delete_account_id_by_id(self, id):
        try:
            cur = self.conn.cursor()

            sql = """
                    DELETE
                    FROM public.account
                    WHERE id = %s
            """

            cur.execute(sql,
                        (id,))


            self.conn.commit()
            cur.close()

        except (Exception, psycopg2.Error) as error:
            print(error)


    def exists_account_by_login(self, login):
        try:
            cur = self.conn.cursor()

            sql = """
                    SELECT login
                    FROM public.account
                    WHERE login = %s
            """

            cur.execute(sql,
                        (login,))

            records = cur.fetchall()
            cur.close()

            if records:
                return True
            else:
                return False

        except (Exception, psycopg2.Error) as error:
            print(error)

    def exists_account_by_id(self, id):
        try:
            cur = self.conn.cursor()

            sql = """
                    SELECT id
                    FROM public.account
                    WHERE id = %s
            """

            cur.execute(sql,
                        (id,))

            records = cur.fetchall()
            cur.close()

            if records:
                return True
            else:
                return False

        except (Exception, psycopg2.Error) as error:
            print(error)


postgresql = ConnectionPostgreSQL()
