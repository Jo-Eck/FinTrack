import streamlit as st
import streamlit_authenticator as stauth
import requests

LOGIN_URL = 'http://localhost:8888/login'

def login(username, password):
    """
    Sends a post request to the pre-specified URL
    * logs in user if username + password are correct

    Param:
        username (string): Name of user
        password (string): Password of user
    """
    json = {'username' : f'{username}', 'password' : f'{password}'}
    if username is not None:
        r = requests.post(LOGIN_URL, json)
    st.write(r.text)
    
st.title("Login")
username = st.text_input(label="Username")
password = st.text_input(label="Password", type="password")
login_btn = st.button(label="Login")
if login_btn:
    if(login(username, password)) == "Login Success :D":
        st.session_state["auth_status"] = True
    else:
        st.session_state["auth_status"] = False