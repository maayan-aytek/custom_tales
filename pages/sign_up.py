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
set_logo(logo_width="20", margin_left="800", margin_bottom="-170")
set_button(buttons_right="-217", margin_top="50")
set_text_input(width="350", margin_bottom="-30")
set_number_input(width="20", margin_bottom="-5")
set_selectbox_input(width="350", margin_bottom="-5")
db = get_db_connection()

col1, col2, col3 = st.columns([0.18, 0.7, 0.12])
with col1:
    st.write("")
with col2:
    st.write("### Please fill here your child information:")
with col3:
    st.write("")

user_name = st.text_input("username", placeholder="")
password = st.text_input("password", type="password", placeholder="", help="""Passwords should contain three of the four character types:\n\nUppercase letters: A-Z\n\nLowercase letters: a-z\n\nNumbers: 0-9""")
name = st.text_input("Name", placeholder="")
gender = st.selectbox("Gender", options=["Male", "Female", "Prefer not to say"])
age = st.text_input("Age", placeholder="")
interests = st.text_input("Interests", placeholder="E.g: football, science, princesses, cars, painting...")
