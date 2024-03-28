import streamlit as st
import json
from google.cloud import firestore
from utils import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
set_logo(logo_width=40, margin_left=170)
set_button(buttons_right="-217", margin_top="50")
set_text_input()
db = get_db_connection()

user_name = st.text_input("", placeholder="username")
password = st.text_input("", type="password", placeholder="password")
is_click_login = st.button("# Login")


if is_click_login:
    all_users = db.collection('users').get()
    incorrect_details = False
    for user in all_users:
        if user.id == user_name:
            user_dict = db.collection('users').document(user.id).get().to_dict()
            if user_dict["password"] == password:
                st.session_state['USERNAME'] = user_name
                st.session_state['NAME'] = user_dict['general_information']['name']
                st.session_state['AGE'] = user_dict['general_information']['age']
                st.session_state['GENDER'] = user_dict['general_information']['gender']
                st.session_state['INTERESTS'] = user_dict['general_information']['interests']
                switch_page("home")
                break

    incorrect_details = True
    if incorrect_details:
        st.markdown("""  
        <style>  
            .stAlert[data-st-id="warning"] {  
            }  
        </style>  
        """, unsafe_allow_html=True)
        st.warning("Incorrect username or password. Please try again.", icon="⚠️")



