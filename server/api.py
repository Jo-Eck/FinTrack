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
    with get_explorer() as explorer:
        return explorer.get_last_transactions()


@app.get('/categories')
def get_categories():
    with get_explorer() as explorer:
        return explorer.get_categories()


@app.post('/api')
def create_new_transaction():
    """Calls for a new Trasnaction to be inserted into the Database with the recieved Jsons"""
    jsondata = request.json
    with get_explorer() as explorer:
        explorer.insert_transaction(
            jsondata.get("name"),
            jsondata.get("description"),
            jsondata.get("category"),
            jsondata.get("value"))
        return ({}, 200)


if __name__ == '__main__':
    app.run(
        conf.get('Flask', 'API_HOST'),
        conf.get('Flask', 'API_PORT'),
        conf.get('Flask', 'API_DEBUG'),)
