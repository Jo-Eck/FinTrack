import streamlit as st
import streamlit_authenticator as stauth
import requests

LOGIN_URL = 'http://localhost:8888/login'

def login(username, password):
    """
    
    Sends a post request to the pre-specified URL

    Param:
        name (string): Name of the transaction
        desc (string): Descripton for the transaction
        value (float): The monitary value
        category (string): category of the transaction
        user (string): The loggin user
    """
    json = {'username' : f'{username}', 'password' : f'{password}'}
    if username is not None:
        r = requests.post(LOGIN_URL, json)
    st.write(r.text)
    
st.title("Login")
username = st.text_input(label="Username")
password = st.text_input(label="Description")
login_btn = st.button(label="Save")
if login_btn:
    login(username, password)