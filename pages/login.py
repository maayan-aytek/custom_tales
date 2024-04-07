import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container


# page and styling configurations 
st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_logo(logo_width=40, margin_left=170)
set_button(buttons_right="-217", margin_top="50")
set_text_input()
db = get_db_connection()

# Setting home button
b64_home_string = set_image_porperties(os.path.join('photos', 'home_button_image.png'), image_resize=0.06, x_padding=-8, y_padding=-8)
col01, col02, col03 = st.columns([0.05,0.05,0.8])
with col02:
    with stylable_container(
        "home",
        css_styles = set_image_circle_button(b64_home_string, margin_left='-650', margin_top='-260')
    ):
        is_click_home = st.button(label='', key='button2')
        if is_click_home:
            switch_page('main')

# Setting buttons 
user_name = st.text_input("", placeholder="username")
password = st.text_input("", type="password", placeholder="password")
is_click_login = st.button("# Login")


if is_click_login:
    # Verify the user username and password
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



