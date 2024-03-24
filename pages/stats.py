import streamlit as st
import json
from google.cloud import firestore
from utils import *
import pandas as pd 
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
set_text_input(width="280", margin_bottom="-30", margin_left='210')
set_selectbox_input(width="280", margin_bottom="0", margin_left='210')

b64_gen_story_string = set_image_porperties(path=rf'photos/generate_story_image.png', image_resize=0.105, x_padding=-10, y_padding=-13)
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.06, x_padding=-8, y_padding=-8)

col1, col2, col3 = st.columns([0.05,0.05,0.8])
with col2:
    with stylable_container(
        "home",
        css_styles = set_image_circle_button(b64_home_string, margin_left='-230', margin_top='-90'),
    ):
        is_click_home = st.button(label='', key='button2')
        if is_click_home:
            switch_page('home')
with col3:
    set_logo(margin_left="100", margin_bottom="-20")



