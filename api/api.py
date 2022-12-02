"""Provides a Flask-API for the database"""

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash

import db_explorer
import os

app = Flask(__name__)
auth = HTTPBasicAuth()


def get_explorer():
    """Returns an object of the Database Explorer"""
    return db_explorer.DbExplorer()


@app.route('/')
def index():
    """
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
    >>> get_transaction()
    ""
    """
    with get_explorer() as explorer:
        return explorer.get_last_transactions(request.json["username"])


@app.post('/new_transaction')
@auth.login_required
def create_new_transaction():
    """
    Calls for a new Trasnaction to be inserted into the Database with the
    recieved Jsons
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
    >>> delete_transaction()
    ""
    """
    json = request.json
    with get_explorer() as explorer:
        explorer.delete_transaction(json["id"])
        return ("Success", 200)


@app.get('/categories')
@auth.login_required
def get_categories():
    """
    Returns all the categories
    >>> get_categories()
    "Entertainment, Lebensmittel"
    """
    with get_explorer() as explorer:
        return explorer.get_categories()


@app.get('/users')
@auth.login_required
def get_users():
    """
    Returns all the usernames
    >>> get_users()
    ""
    """
    with get_explorer() as explorer:
        return explorer.get_users()


@app.post('/login')
def login():
    """
    Checks if a specific username and password combination exists 
    >>> login()
    ""
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
    Creates a new user in the database
    >>> signup_post()
    ""
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
    >>> verify_password('Jin', '1234')
    Jin
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
