import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
import plotly.express as px

st.title('Financial Tracker 3000')

col1, col2, col3  = st.columns(3)
GET_URL = 'http://localhost:8888/transactions'
POST_URL = 'http://localhost:8888/new_transaction'

balance = 0.00
user_name = "Jan"

def load_transactions():
    trans = requests.get(GET_URL).json()
    return trans

def post_transaction(name, desc, value, category, user):
    json = {'name' : f'{name}', 'description' : f'{desc}'
            , 'category' : f'{category}' , 'value' : f'{value}', 'username' : f'{user}'}
    if name is not None:
        r = requests.post(POST_URL, json)
    st.write(r.text)

table_data = pd.DataFrame(
            load_transactions(),
            columns=["Id","Name", "Desc", "Category", "Date", "Value", "User"])

with col1:
    st.subheader('Balance')
    st.write(balance)
        
with col2:
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
    st.table(table_data)
