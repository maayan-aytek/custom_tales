import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_logo(logo_width="20", margin_left="800", margin_bottom="-270")
set_button(buttons_right="-270", margin_top="20")
set_text_input(width="350", margin_bottom="-30")
set_number_input(width="20", margin_bottom="-5")
set_selectbox_input(width="350", margin_bottom="-5")
db = get_db_connection()


def is_validate_details(user_name, password, name, gender, age, interests, db):
    if not all([user_name, password, name, gender, age, interests]):
        st.warning("Please fill in all fields.", icon="⚠️")
        return False

    all_users = [user.id for user in db.collection('users').get()]
    if user_name in all_users:
        st.warning("Username alreay exists in the system. Please choose other username.", icon="⚠️")
        return False
    
    if not any(c.isupper() for c in password) or \
       not any(c.islower() for c in password) or \
       not any(c.isdigit() for c in password):
        st.warning("Password should contain at least one Upper case letters: A-Z, one Lowercase letters: a-z, and one Number: 0-9.", icon="⚠️")
        return False
    

    if not age.isdigit() or int(age) <= 0:
        st.warning("Age must be a positive integer.", icon="⚠️")
        return False

    return True


col1, col2, col3 = st.columns([0.18, 0.7, 0.12])
with col1:
    st.write("")
with col2:
    st.write("### Please fill here your child information:")
with col3:
    st.write("")

user_name = st.text_input("username", placeholder="")
password = st.text_input("password", type="password", placeholder="", help="""Passwords should contain the following character types:\n\nUppercase letters: A-Z\n\nLowercase letters: a-z\n\nNumbers: 0-9""")
name = st.text_input("Name", placeholder="")
gender = st.selectbox("Gender", options=["Male", "Female", "Prefer not to say"], placeholder="")
age = st.text_input("Age", placeholder="")
interests = st.text_input("Interests", placeholder="E.g: football, science, princesses, cars, painting...", help="Enter your child's interests separated by commas. You can write one or multiple interests.")

is_click_register = st.button("# Register")
if is_click_register:
    if is_validate_details(user_name, password, name, gender, age, interests, db):
        db_ref = db.collection("users").document(user_name)
        db_ref.set({
            "general_information":
            {
            "name": name,
            "gender": gender,
            "age": age,
            "interests": interests
            }, 
            "password": password
        })
        st.session_state['USERNAME'] = user_name
        st.session_state['NAME'] = name
        st.session_state['AGE'] = age
        st.session_state['GENDER'] = gender
        st.session_state['INTERESTS'] = interests
        switch_page("home")



