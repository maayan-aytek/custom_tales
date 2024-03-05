import streamlit as st
import json
from google.cloud import firestore
from utils import set_background, get_base64, init_page, get_db_connection
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')

init_page()
db = get_db_connection()

