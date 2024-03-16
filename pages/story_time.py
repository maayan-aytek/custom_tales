import streamlit as st
import json
from google.cloud import firestore
from utils import *
import pandas as pd 
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
set_logo()
set_text_input(width="280", margin_bottom="-30")
set_selectbox_input(width="280", margin_bottom="0")

b64_gen_story_string = set_image_porperties(path=rf'photos/generate_story_image.png', image_resize=0.1, x_padding=-12, y_padding=-12)
b64_back_string = set_image_porperties(path=rf'photos/back.png', image_resize=0.05, x_padding=-8, y_padding=-8)
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.05, x_padding=-8, y_padding=-8)


# is_click_back = st.button(label='', key='story_time - back')
# set_image_circle_button(b64_back_string, button_id='story_time - back', margin_left='20')
# if is_click_back:
#     pass

# is_click_home = st.button(label='', key='story_time - home')
# set_image_circle_button(b64_home_string, button_id='story_time - home', margin_left='40')
# if is_click_home:
#     switch_page('home')

def is_validate_details(reading_time, moral, mode):
    if not all([reading_time, moral, mode]):
        st.warning("Please fill in all fields.", icon="⚠️")
        return False

    if not reading_time.isdigit() or int(reading_time) <= 0:
        st.warning("Reading Time must be a positive integer.", icon="⚠️")
        return False

    return True


col1, col2, col3 = st.columns([0.05, 0.6, 0.01])
with col1:
    st.write("")
with col2:
    st.write(f"### Before we dive in, fill in the details about your story")
with col3:
    st.write("")


books_df = pd.read_csv('books_data.csv')

reading_time = st.text_input("Reading Time (min)", placeholder="")
moral = st.text_input("Moral", placeholder="E.g. Be kind")
mode = st.selectbox("Mode", options=["Classic", "Creative", "Innovative"], placeholder="")
main_character_name = st.text_input("Main Character Name", placeholder="", help="If not provided, the main character name will default to the child's name.")
similar_story = st.selectbox("Story Inspiration", options=['Ignored'] + list(books_df['Name'].drop_duplicates().sort_values()), help="Select the story template or framework to use as a basis when creating a new story.\n\nIf you're unsure which template to choose, you can leave this field as 'ignored', and a new story will be created from scratch.")

set_image_circle_button(b64_gen_story_string, margin_left='100')
is_click_generate_story = st.button(label='',key="story_time - generate_story")

if is_click_generate_story:
    if is_validate_details(reading_time, moral, mode):
        st.session_state['story_details'] = {'reading_time': reading_time,
                                             'moral': moral,
                                             'mode': mode,
                                             'main_character_name': st.session_state['NAME'] if main_character_name == '' else main_character_name,
                                             'similar_story': similar_story,
                                             }
        switch_page("choose_story")

