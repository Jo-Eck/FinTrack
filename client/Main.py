import streamlit as st
import requests
import pandas as pd


LOGIN_URL = 'http://localhost:8888/login'
GET_URL = 'http://localhost:8888/transactions'
POST_URL = 'http://localhost:8888/new_transaction'


def load_transactions():
    """
    makes a get request to fetch all transactions

    Returns:
        list: list of all transactions
    """
    trans = requests.get(GET_URL).json()
    return trans


def count_transactions():
    """
    Counts all transactions

    Returns:
        int: sum of transactions
    """
    x = 0
    for i in load_transactions():
        x += 1
    return x


def calc_balance(data):
    """
    Calculates the balance after all transactions
    """
    balance = 0.0
    for i in data['Value']:
        balance += i
    return balance


def post_transaction(name, desc, value, category, user):
    """

    Sends a post request to the pre-specified URL

    Param:
        name (string): Name of the transaction
        desc (string): Descripton for the transaction
        value (float): The monitary value
        category (string): category of the transaction
        user (string): The loggin user
    """
    json = {'name': name,
            'description': desc,
            'value': value,
            'category': category,
            'username': user}

    if name is not None:
        r = requests.post(url=POST_URL, json=json)
    st.write(r.text)


def check_credentials(username, password):
    """
    Sends a post request to the pre-specified URL
    * logs in user if username + password are correct

    Param:
        username (string): Name of user
        password (string): Password of user
    """
    json = {'username': f'{username}', 'password': f'{password}'}

    if username is not None:
        return requests.post(LOGIN_URL, json).status_code

    return None


def page_dashboard():
    transactions = requests.post(API + "/transactions" , json= {"username": st.session_state.user}).json()
    data = pd.DataFrame(
        load_transactions(),
        columns=["Id", "Name", "Desc", "Category", "Date", "Value", "User"])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Balance')
        st.write(calc_balance(data))

    with col2:
        st.write("Enter a new Transaction:")
        name = st.text_input(label="Name")
        desc = st.text_input(label="Description")
        category = st.text_input(label="Category:")
        value = st.text_input(label="Value:", placeholder="€")
        user = st.session_state.user
        save = st.button(label="Save")
        if save:
            st.write("Your Transaction will be saved")
            post_transaction(name, desc, value, category, user)
            st.experimental_rerun()

    with col3:
        if st.button("Reload"):
            st.experimental_rerun()
        st.write(f"Your past transactions: {count_transactions()}")
        st.table(data)


def page_login():
    st.title("Login")
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")
    login_btn = st.button(label="Login")

    if login_btn:
        if (check_credentials(username, password)) == 200:
            st.session_state["auth_status"] = True
            st.session_state.runpage = page_dashboard
            st.experimental_rerun()
        else:
            st.session_state["auth_status"] = False
            st.warning("Username or Password not correct!")

    if st.button(label="You dont have an account?"):
        st.session_state.runpage = page_registration
        st.experimental_rerun()


def page_registration():
    st.title("Registration")


if 'runpage' not in st.session_state:
    st.session_state.runpage = page_login
    st.experimental_rerun()

if st.session_state.runpage is not page_login:
    if st.button(label="Go Home"):
        st.session_state.runpage = page_login

st.session_state.runpage()
