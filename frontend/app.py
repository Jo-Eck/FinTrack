"""Provides a web-based interface for the user to interact with the API"""
import os
import pandas as pd
import requests
import streamlit as st


API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")


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
        response = requests.post(
            url=f"http://{API_HOST}:{API_PORT}/new_transaction",
            json=json,
            auth=(
                st.session_state["user"],
                st.session_state["password"]),
            timeout=10)
    st.write(response.text)


def page_dashboard():
    """Dashboard Page"""
    transactions = requests.post(
        url=f"http://{API_HOST}:{API_PORT}/transactions",
        json={"username": st.session_state["user"]},
        auth=(
                st.session_state["user"],
                st.session_state["password"]),
        timeout=10,
    ).json()

    transaction_table = pd.DataFrame(
        transactions,
        columns=["Name", "Desc", "Category", "Date", "Value"])

    if st.button(label="Logout"):
        st.session_state.runpage = page_login
        st.session_state["auth_status"] = False
        st.session_state["user"] = None
        st.session_state["password"] = None
        st.experimental_rerun()

    st.title("Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('Balance')
        st.write(sum(i[4] for i in transactions))

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
        st.table(transaction_table)


def page_login():
    """Login Page"""
    st.title("Login")
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")
    login_btn = st.button(label="Login")

    if login_btn:
        if (
            requests.post(
                url=f"http://{API_HOST}:{API_PORT}/login",
                json={"username": username, "password": password},
                timeout=10
            ).status_code
        ) == 200:

            st.session_state["auth_status"] = True
            st.session_state["user"] = username
            st.session_state["password"] = password
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
                url=f"http://{API_HOST}:{API_PORT}/register",
                json={"username": username, "password": password},
                timeout=10
            )
            st.session_state["user"] = username
            st.session_state["password"] = password
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
