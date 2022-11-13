"""Provides a web-based interface for the user to interact with the API"""

import configparser as cp

import pandas as pd
import requests
import streamlit as st

conf = cp.ConfigParser()
conf.read("config.ini")
API = f"http://{conf.get('Flask', 'API_HOST')}:{conf.get('Flask', 'API_PORT')}"


def post_transaction(name, desc, value, category):
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
            'username': st.session_state["user"]}

    if name is not None:
        response = requests.post(url=API + "/new_transaction",
                                 json=json,
                                 timeout=10)
    st.write(response.text)


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
        return requests.post(API+"/login", json, timeout=10).status_code

    return None


def page_dashboard():
    """Dashboard Page"""
    transactions = requests.post(
        API + "/transactions",
        json={"username": st.session_state["user"]},
        timeout=10
    ).json()
    data = pd.DataFrame(
        transactions,
        columns=["Id", "Name", "Desc", "Category", "Date", "Value", "User"])

    if st.button(label="Logout"):
        st.session_state.runpage = page_login
        st.session_state["auth_status"] = False
        st.session_state["user"] = None
        st.experimental_rerun()

    st.title("Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Balance')
        st.write(sum(i[5] for i in transactions))

    with col2:
        st.write("Enter a new Transaction:")
        name = st.text_input(label="Name")
        desc = st.text_input(label="Description")
        category = st.text_input(label="Category:")
        value = st.text_input(label="Value:", placeholder="€")
        save = st.button(label="Save")
        if save:
            st.write("Your Transaction will be saved")
            post_transaction(name, desc, value, category)
            st.experimental_rerun()

    with col3:
        if st.button("Reload"):
            st.experimental_rerun()
        st.write(
            f"Your past transactions: {len(transactions)}")
        st.table(data)


def page_login():
    """Login Page"""
    st.title("Login")
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")
    login_btn = st.button(label="Login")

    if login_btn:
        if (check_credentials(username, password)) == 200:
            st.session_state["auth_status"] = True
            st.session_state["user"] = username
            st.session_state.runpage = page_dashboard
            st.experimental_rerun()
        else:
            st.session_state["auth_status"] = False
            st.warning("Username or Password not correct!")

    if st.button(label="You dont have an account?"):
        st.session_state.runpage = page_registration
        st.experimental_rerun()


def page_registration():
    """Registration Page"""
    st.title("Registration")
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")
    password2 = st.text_input(label="Repeat Password", type="password")
    register_btn = st.button(label="Register")

    if register_btn:
        if password == password2:
            st.session_state["auth_status"] = True
            requests.post(
                API + "/register",
                json={"username": username, "password": password},
                timeout=10
            )
            st.session_state["user"] = username
            st.session_state.runpage = page_dashboard
            st.experimental_rerun()
        else:
            st.session_state["auth_status"] = False
            st.warning("Passwords do not match!")

    if st.button(label="You already have an account?"):
        st.session_state.runpage = page_login
        st.experimental_rerun()


if 'runpage' not in st.session_state:
    st.session_state.runpage = page_login
    st.experimental_rerun()

if st.session_state.runpage is not page_login:
    if st.button(label="Go Home"):
        st.session_state.runpage = page_login

st.session_state.runpage()
