"""Provides a Flask-API for the database"""
import os
import db_explorer

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash


app = Flask(__name__)
auth = HTTPBasicAuth()


def get_explorer():
    """Returns an object of the Database Explorer"""
    return db_explorer.DbExplorer()


@app.route('/')
def index():
    """
    Testing methodology: Setup TestDB with clean-slate information.
    Execute index with known parameters and compare output with expected values.
    Input: None (no input)
    Output: 'Whats up' page
    Front Page
    >>> index()
    "Whats up?"
    """
    return "Whats up?"


@app.post('/transactions')
@auth.login_required
def get_transactions():
    """
    Returns all the transactions in the database for a given user

    Testing methodology: Setup TestDB with clean-slate information.
    Execute get_transactions with known parameters and compare output with expected values.
    Login the test-user. Test-users transactions are known, execute get_transactions and
    compare returned values with known data for test user.
    >>> get_transactions()
    "Set of transactions for logged in user"
    """
    with get_explorer() as explorer:
        return explorer.get_last_transactions(request.json["username"])


@app.post('/new_transaction')
@auth.login_required
def create_new_transaction():
    """
    Calls for a new Transaction to be inserted into the Database with the
    received Json-strings
        Testing methodology: Setup TestDB with clean-slate information.
    Execute create_new_transaction with known parameters
    and compare output with expected values via get_transactions afterwards.
    >>> create_new_transaction()
    "Transaction inserted", 200
    """
    json = request.json
    try:
        with get_explorer() as explorer:
            if json["category"] not in get_categories():
                explorer.create_category(json["category"], "")
            explorer.insert_transaction(json)
    except KeyError:
        return "Missing parameters", 400
    return "Transaction inserted", 200


@app.post('/delete_transaction')
@auth.login_required
def delete_transaction():
    """
    Deletes a transaction from the database
    Testing methodology: Setup TestDB with clean-slate information.
    Execute delete_transaction with previously inserted transaction,
    check that transaction has been removed using get_transactions afterwards.
    >>> delete_transaction()
    "Success"
    """
    json = request.json
    with get_explorer() as explorer:
        explorer.delete_transaction(json["id"])
        return ("Success", 200)


@app.get('/categories')
@auth.login_required
def get_categories():
    """
    Returns all the categories in the database.

    Testing methodology: Setup TestDB with clean-slate information.
    Insert known categories into the database.
    Execute get_categories and compare output expected values.
    >>> get_categories()
    "Set of known categories"
    """
    with get_explorer() as explorer:
        return explorer.get_categories()


@app.get('/users')
@auth.login_required
def get_users():
    """
    Returns all the usernames in the database.

    Testing methodology: Setup TestDB with clean-slate information.
    Insert known users into the database.
    Execute get_users and compare output with expected values.
    >>> get_users()
    "set of known users"
    """
    with get_explorer() as explorer:
        return explorer.get_users()


@app.post('/login')
def login():
    """
    Checks if a specific username and password combination exists
    Testing methodology:
    Setup TestDB with clean-slate information.
    Execute login() and compare output with expected values.
    Test with valid login information:
    >>> login()
    ("",200)
    Test with invalid login information:
    >>> login()
    ("",401)
    """
    username = request.form.get('username')
    password = request.form.get('password')

    with get_explorer() as explorer:
        if not explorer.check_user_existence(username):
            return ("", 401)
        if explorer.check_password(username, password):
            return ("", 200)
    return ("", 401)


@app.route('/register', methods=['POST'])
def signup_post():
    """
    Creates a new user in the database:
    Testing methodology:
    Setup TestDB with clean-slate information.
    Execute signup_post() and compare output with expected values.
    >>> signup_post()
    "User created", 200
    """
    json = request.json
    username = json["username"]
    password = generate_password_hash(json["password"])
    try:
        with get_explorer() as explorer:
            if explorer.check_user_existence(username):
                return "Username already taken"
            explorer.create_user(username, password)
            return "User created", 200
    except KeyError:
        return "Missing parameters", 400


@auth.verify_password
def verify_password(username, password):
    """
    Checks if a username and password combination exists
    Testing methodology:
    Setup TestDB with clean-slate information.
    Execute verify_password() with known parameters and
    compare output with expected values.
    Test with valid data:
    >>> verify_password('Jin', '1234')
    "Jin"
    Test with invalid data:
    >>> verify_password('Jan', 'XYZ')
    "None"
    """
    with get_explorer() as explorer:
        if (explorer.check_password(username, password)
                and explorer.check_user_existence(username)):
            return username
    return None


if __name__ == '__main__':
    app.run(
        os.getenv("API_HOST"),
        os.getenv("API_PORT"),
        os.getenv("API_Debug")
    )
