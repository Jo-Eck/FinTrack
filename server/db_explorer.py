import configparser as cp
import psycopg2


class DbExplorer:
    """Class to interface with the Database"""

    def __init__(self):
        self.conf = cp.ConfigParser()
        self.conn = None

    def __enter__(self):

        self.conf.read("config.ini")

        print('Connecting to the PostgreSQL database...')
        self.conn = psycopg2.connect(
            host=self.conf.get('Postgres', 'DB_HOST'),
            database=self.conf.get('Postgres', 'DB_NAME'),
            user=self.conf.get('Postgres', 'DB_USER'),
            password=self.conf.get('Postgres', 'DB_PASSWORD'))
        return self

    def __exit__(self, exeption_type, exeption_value, traceback):
        self.conn.close()

    def insert_transaction(self,  name, description, category, value, username):
        """"inserts new transaction into the Database"""

        try:
            cur = self.conn.cursor()

            sql = f"""INSERT INTO fintrackschema.transactions  VALUES(DEFAULT,
                        '{name}', '{description}', '{category}', DEFAULT, '{value}','{username}');"""

            cur.execute(sql)
            self.conn.commit()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def insert_category(self, name, description):
        """Inserts a new kind of category to the Database"""
        try:
            cur = self.conn.cursor()

            sql = f"""INSERT INTO fintrackschema.categories VALUES('{name}', '{description}');"""

            cur.execute(sql)
            self.conn.commit()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_last_transactions(self, amount=None):
        """Provides the last N Trasnactions form the Database,
            if no number of transactions is given it returns all"""

        try:
            cur = self.conn.cursor()
            sql = None

            if amount is not None:
                sql = f"""select * from fintrackschema.transactions limit {amount};"""
            else:
                sql = """select * from fintrackschema.transactions;"""

            cur.execute(sql)
            return cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def get_categories(self):
        """Provides all categories from the database"""

        try:
            cur = self.conn.cursor()
            sql = """select * from fintrackschema.categories;"""

            cur.execute(sql)
            return cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def get_users(self):
        """Provides all usernames from the database"""

        try:
            cur = self.conn.cursor()
            sql = """select user_name from fintrackschema.users;"""

            cur.execute(sql)
            return cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def check_user_existance(self, name):
        """Checks if useraccount """
        try:
            cur = self.conn.cursor()
            sql = f"""select * from fintrackschema.users WHERE user_name = '{name}' ;"""

            cur.execute(sql)
            return cur.fetchone() is not None

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return None

    def create_user(self, name, password):
        """Creates a new user in the database"""
        try:
            cur = self.conn.cursor()

            sql = f"""INSERT INTO fintrackschema.users  VALUES('{name}','{password}');"""

            cur.execute(sql)
            self.conn.commit()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
