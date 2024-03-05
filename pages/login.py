import streamlit as st
import json
from google.cloud import firestore
from utils import set_background, get_base64, init_page, get_db_connection
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')

init_page()
db = get_db_connection()

st.markdown("""  
<style>  
    .stTextInput input {  
        color: white;  
        height: 45px;
        border-radius: 25px;  
        backgroud-color: lightgray;
    }  
    
    .stTextInput {
        width: 250px;
        height: 100px;
        margin-left: 190px; 
        margin-bottom: -55px;
    }
</style>  
""", unsafe_allow_html=True)

user_name = st.text_input("", placeholder="username")
password = st.text_input("", type="password", placeholder="password")

if user_name and password:
    all_users = db.collection('users').get()
    incorrect_details = False
    for user in all_users:
        if user.id == user_name:
            user_dict = db.collection('users').document(user.id).get().to_dict()
            if user_dict["password"] == password:
                switch_page("main")
                break

    incorrect_details = True
    if incorrect_details:
        st.markdown("""  
        <style>  
            .stAlert[data-st-id="warning"] {  
            }  
        </style>  
        """, unsafe_allow_html=True)
        st.warning("⚠️ Incorrect username or password. Please try again.")
# help="""Passwords should contain three of the four character types:\n\nUppercase letters: A-Z\n\nLowercase letters: a-z\n\nNumbers: 0-9""")

