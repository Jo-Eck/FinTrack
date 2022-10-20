import configparser as cp
import db_explorer
from flask import(Flask, request)

app = Flask(__name__)

conf = cp.ConfigParser()
conf.read("config.ini")


def get_explorer():
    """Returns an object of the Database Explorer"""
    return db_explorer.DbExplorer()


@app.route('/')
def index():
    """Front Page"""
    return("Whats up?")


@app.get('/transactions')
def get_transactions():
    """Returns all the transactions in the database"""
    with get_explorer() as explorer:
        return explorer.get_last_transactions()


@app.get('/categories')
def get_categories():
    """Returns all the categories"""
    with get_explorer() as explorer:
        return explorer.get_categories()


@app.get('/users')
def get_users():
    """Returns all the usernames"""
    with get_explorer() as explorer:
        return explorer.get_users()


@app.post('/new_transaction')
def create_new_transaction():
    """Calls for a new Trasnaction to be inserted into the Database with the recieved Jsons"""
    jsondata = request.json
    with get_explorer() as explorer:
        explorer.insert_transaction(
            jsondata.get("name"),
            jsondata.get("description"),
            jsondata.get("category"),
            jsondata.get("value"),
            jsondata.get("username"))
# TODO implement propper return codes
        return ({}, 200)


@app.route('/login')
def login():

    return 'Login'


@app.route('/signup', methods=['POST'])
def signup_post():

    username = request.form.get("username")
    password = request.form.get("password")

    with get_explorer() as explorer:

        if explorer.check_user_existance(username):
            return "Username already taken"
        explorer.create_user(username, password)
        return ("Success :D", 200)
        # TODO implemnt proper return codes


@app.route('/logout')
def logout():
    return 'Logout'


if __name__ == '__app__':
    app.run(
        conf.get('Flask', 'API_HOST'),
        conf.get('Flask', 'API_PORT'),
        conf.get('Flask', 'API_DEBUG'),)
