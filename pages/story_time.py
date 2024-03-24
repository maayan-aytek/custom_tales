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
# b64_back_string = set_image_porperties(path=rf'photos/back.png', image_resize=0.2, x_padding=-6, y_padding=-6)
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

user_name = st.session_state['USERNAME']
reading_time = st.text_input("Reading Time (min)", placeholder="")
moral = st.text_input("Moral", placeholder="E.g. Be kind")
mode = st.selectbox("Mode", options=["Classic", "Creative", "Innovative"], placeholder="")
main_character_name = st.text_input("Main Character Name", placeholder="", help="If not provided, the main character name will default to the child's name.")
similar_story = st.selectbox("Story Inspiration", options=['Ignored'] + list(books_df['Name'].drop_duplicates().sort_values()), help="Select the story template or framework to use as a basis when creating a new story.\n\nIf you're unsure which template to choose, you can leave this field as 'ignored', and a new story will be created from scratch.")

with stylable_container(
    "generate_story",
    css_styles = set_image_circle_button(b64_gen_story_string, radius='11', margin_left='300'),
):
    is_click_generate_story = st.button(label='',key="story_time - generate_story")


if is_click_generate_story:
    if is_validate_details(reading_time, moral, mode):
        st.session_state['story_details'] = {'reading_time': reading_time,
                                            'moral': moral,
                                            'mode': mode,
                                            'main_character_name': st.session_state['NAME'] if main_character_name == '' else main_character_name,
                                            'similar_story': similar_story,
                                            }
        st.session_state['is_story_1_clicked'] = False
        st.session_state['is_story_2_clicked'] = False
        st.session_state['is_story_3_clicked'] = False
        st.session_state['is_clicked_choose_story'] = False
        st.session_state['stories'] = None
        switch_page("choose_story")

        

