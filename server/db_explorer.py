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

    def insert_transaction(self, category,  name, description, value):
        """"inserts new transaction into the Database"""

        try:
            cur = self.conn.cursor()

            sql = f"""INSERT INTO fintrackschema.transactions  VALUES(DEFAULT,
                        '{category}', '{name}', '{description}' DEFAULT, '{value}',);"""

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
