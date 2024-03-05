import streamlit as st
from utils import set_background, get_base64, init_page
from streamlit_extras.switch_page_button import switch_page



st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')

init_page(logo_width=300, buttons_right="-215")
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col1:
    st.write("")
with col2:
    st.title("Welcome to CustomTales!")
with col3:
    st.write("")

is_clicked_about = st.button("# About Us")
is_click_login = st.button("# Login")
is_click_sign_up = st.button("# Sign Up")

if is_clicked_about:
    switch_page("about")
if is_click_sign_up:
    switch_page("sign_up")
if is_click_login:
    switch_page("login")
    

    
