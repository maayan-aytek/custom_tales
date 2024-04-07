import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page



st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_logo_wa_position(logo_width=40)
set_button_wa_position()

# Main inital page in the app
st.markdown(f'<h1 style="text-align: center;">Welcome to CustomTales!</h1>', unsafe_allow_html=True)

# buttons definitions
is_clicked_about = st.button("# About Us")
is_click_login = st.button("# Login")
is_click_sign_up = st.button("# Sign Up")

# switch to other pages
if is_clicked_about:
    switch_page("about")
if is_click_sign_up:
    switch_page("sign_up")
if is_click_login:
    switch_page("login")
    

    
