""" Interface for financial tracker

    author: JANR
    date:
    version: 0.0.1
    licence: free
"""

import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
import requests

st.title('Financial Tracker')

col1, col2, col3  = st.columns(3)

GET_URL = 'http://localhost:8888/transactions'
POST_URL = 'http://localhost:8888/new_transaction'
user_name = "Jan"

def load_transactions():
    """
    makes a get request to fetch all transactions

    Returns:
        list: list of all transactions
    """
    trans = requests.get(GET_URL).json()
    return trans

data = pd.DataFrame(
            load_transactions(),
            columns=["Id","Name", "Desc", "Category", "Date", "Value", "User"])

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

def calc_balance():
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
    json = {'name' : f'{name}', 'description' : f'{desc}'
            , 'category' : {category} , 'value' : f'{value}', 'username' : f'{user}'}
    if name is not None:
        r = requests.post(POST_URL, json)
    st.write(r.text)


with col1:
    """
    shows the user his total balance based on the past transactions
    """
    st.subheader('Balance')
    st.write(calc_balance())
        
with col2:
    """
    enables user to enter new transaction
    """
    st.write("Enter a new Transaction:")
    name = st.text_input(label="Name")
    desc = st.text_input(label="Description")
    category = st.text_input(label="Category:")
    value = st.text_input(label="Value:", placeholder="€")
    user = user_name
    save = st.button(label="Save")
    if save:
        st.write(f"Your Transaction will be saved")
        post_transaction(name, desc, category, value, user)

    
with col3:
    """
    shows the table for all transactions
    """
    st.write(f"Your past transactions: {count_transactions()}")
    st.table(data)
