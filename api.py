"""Provides a Flask-API for the database"""

import configparser as cp
from flask import Flask, request
from werkzeug.security import generate_password_hash

import db_explorer

app = Flask(__name__)

conf = cp.ConfigParser()
conf.read("config.ini")


def get_explorer():
    """Returns an object of the Database Explorer"""
    return db_explorer.DbExplorer()


@app.route('/')
def index():
    """Front Page"""
    return "Whats up?"


@app.post('/transactions')
def get_transactions():
    """Returns all the transactions in the database for a given user"""
    with get_explorer() as explorer:
        return explorer.get_last_transactions(request.json["username"])


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
    """Calls for a new Trasnaction to be inserted into the Database with the
    recieved Jsons"""
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
def delete_transaction():
    """Deletes a transaction from the database"""
    json = request.json
    with get_explorer() as explorer:
        explorer.delete_transaction(json["id"])
        return ("Success :D", 200)


@app.post('/login')
def login():
    """Checks if a specific username and password combination exists """
    username = request.form.get('username')
    password = request.form.get('password')

    with get_explorer() as explorer:
        if not explorer.check_user_existance(username):
            return ("", 401)
        if explorer.check_password(username, password):
            return ("", 200)
    return ("", 401)


@app.route('/register', methods=['POST'])
def signup_post():
    """Creates a new user in the database"""
    json = request.json
    username = json["username"]
    password = generate_password_hash(json["password"])
    try:
        with get_explorer() as explorer:
            if explorer.check_user_existance(username):
                return "Username already taken"
            explorer.create_user(username, password)
            return "User created", 200
    except KeyError:
        return "Missing parameters", 400


if __name__ == '__main__':
    app.run(
        conf.get('Flask', 'API_HOST'),
        conf.get('Flask', 'API_PORT'),
        conf.get('Flask', 'API_DEBUG'),)
