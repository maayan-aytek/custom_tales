import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')

set_background(rf'photos/background.png')
set_logo(logo_width=30, margin_left=215)
set_button(buttons_right="-225", margin_top="0")

name = st.session_state['NAME']

col1, col2, col3 = st.columns([0.36, 0.6, 0.01])
with col1:
    st.write("")
with col2:
    st.title(f"Hi {name}!")
with col3:
    st.write("")


is_clicked_story_time = st.button("# Story Time")
is_click_my_stories = st.button("# My Stories")

if is_clicked_story_time:
    switch_page("story_time")
if is_click_my_stories:
    switch_page("stats")