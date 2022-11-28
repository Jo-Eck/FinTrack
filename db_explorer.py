"""Module which enables the api to interface with the Database"""
import configparser as cp
from werkzeug.security import check_password_hash
import psycopg2


class DbExplorer:
    """
    Class to interface with the Database
    """

    def __init__(self):
        self.conf = cp.ConfigParser()
        self.conn = None

    def __enter__(self):

        self.conf.read("config.ini")

        self.conn = psycopg2.connect(
            host=self.conf.get('Postgres', 'DB_HOST'),
            database=self.conf.get('Postgres', 'DB_NAME'),
            user=self.conf.get('Postgres', 'DB_USER'),
            password=self.conf.get('Postgres', 'DB_PASSWORD'))
        return self

    def __exit__(self, exeption_type, exeption_value, traceback):
        self.conn.close()

    def insert_transaction(self, transaction_params):
        """
        inserts new transaction into the Database
        >>> insert_transaction()
        ""
        """
        try:
            cur = self.conn.cursor()
            sql = f"""INSERT INTO fintrackschema.transactions  VALUES(DEFAULT,
                        '{transaction_params["name"]}',
                        '{transaction_params["description"]}',
                        '{transaction_params["category"]}',
                        DEFAULT,
                        '{transaction_params["value"]}',
                        '{transaction_params["username"]}'
                    );"""
            cur.execute(sql)
            self.conn.commit()
            cur.close()
        except (psycopg2.DatabaseError) as error:
            print(error)

    def create_category(self, name, description):
        """
        Inserts a new kind of category to the Database
        >>> create_category()
        ""
        """
        try:
            cur = self.conn.cursor()
            sql = f"""INSERT INTO fintrackschema.categories
                    VALUES('{name}','{description}');"""

            cur.execute(sql)
            self.conn.commit()
            cur.close()

        except (psycopg2.DatabaseError) as error:
            print(error)

    def get_last_transactions(self, user, amount=None):
        """
        Provides the last N Trasnactions form the Database,
        if no number of transactions is given it returns all
        >>> get_last_transactions()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = None

            if amount is not None:
                sql = f"""select
                    transaction_name,
                    transaction_description,
                    transaction_category,
                    TO_CHAR(
                        timestamp,
                        'HH24:MI DD.MM.YY'
                    ),
                    betrag
                    from fintrackschema.transactions
                    where "user" = '{user}'
                    limit{amount};"""
            else:
                sql = f"""select
                    transaction_name,
                    transaction_description,
                    transaction_category,
                    TO_CHAR(
                        timestamp,
                        'HH24:MI DD.MM.YY'
                    ),
                    betrag
                    from fintrackschema.transactions
                    where "user" = '{user}';"""

            cur.execute(sql)
            return cur.fetchall()
        except (psycopg2.DatabaseError) as error:
            print(error)
            return None

    def get_categories(self):
        """
        Provides all categories from the database
        >>> get_categories()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = """select * from fintrackschema.categories;"""

            cur.execute(sql)
            return cur.fetchall()

        except (psycopg2.DatabaseError) as error:
            print(error)
            return None

    def get_users(self):
        """
        Provides all usernames from the database
        >>> get_users()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = """select user_name from fintrackschema.users;"""
            cur.execute(sql)

            return cur.fetchall()

        except (psycopg2.DatabaseError) as error:
            print(error)
            return None

    def check_user_existence(self, username):
        """
        Checks if useraccount
        >>> check_user_existence()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = f"""select * from fintrackschema.users
            WHERE user_name = '{username}' ;"""

            cur.execute(sql)
            return cur.fetchone() is not None

        except (psycopg2.DatabaseError) as error:
            print(error)
            return None

    def check_password(self, username, password):
        """
        Compares a provided password with the password of a given user
        >>> check_password()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = f"""select user_password from fintrackschema.users WHERE
            user_name = '{username}' ;"""

            cur.execute(sql)

            return check_password_hash(cur.fetchone()[0], password)

        except (psycopg2.DatabaseError) as error:
            print(error)
            return None

    def create_user(self, name, password):
        """
        Creates a new user in the database
        >>> create_user()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = f"""INSERT INTO fintrackschema.users
            VALUES('{name}','{password}');"""

            cur.execute(sql)
            self.conn.commit()
            cur.close()

        except (psycopg2.DatabaseError) as error:
            print(error)

    def delete_transaction(self, transaction_id):
        """
        Deletes a transaction from the database
        >>> delete_transaction()
        ""
        """

        try:
            cur = self.conn.cursor()
            sql = f"""delete from fintrackschema.transactions
                    where transaction_id = {transaction_id};"""

            cur.execute(sql)
            self.conn.commit()

            cur.close()
        except (psycopg2.DatabaseError) as error:
            print(error)

    def get_user_balance(self, user):
        """
        Provides the balance of a given user
        >>> get_user_balance()
        ""
        """
        try:
            cur = self.conn.cursor()

            sql = f"""select sum(value) from fintrackschema.transactions
            where "user" = '{user}';"""

            cur.execute(sql)
            return cur.fetchone()[0]

        except (psycopg2.DatabaseError) as error:
            print(error)
            return None
