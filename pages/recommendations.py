import streamlit as st
from utils import *
import pandas as pd 
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.06, x_padding=-8, y_padding=-8)
col1, col2, col3 = st.columns([0.05,0.05,0.8])
with col2:
    with stylable_container(
        "home",
        css_styles = set_image_circle_button(b64_home_string, margin_left='-130', margin_top='-50'),
    ):
        is_click_home = st.button(label='', key='button2')
        if is_click_home:
            switch_page('home')
with col3:
    set_logo(logo_width="13", top="-60", right="-75")



fill_color = "rgba(255, 255, 255, 0.5)"  
set_button(buttons_right="0", margin_top="200", font_size="25", height="200", color=fill_color, border_color="black")
b64_speaker_string = set_image_porperties(path=rf'photos/speaker_button_image.png', image_resize=0.19, x_padding=-17, y_padding=-9)
b64_back_string = set_image_porperties(path=rf'photos/back.png', image_resize=0.2, x_padding=-6, y_padding=-6)
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.06, x_padding=-8, y_padding=-8)

chosen_story = st.session_state['chosen_story']
chosen_story_embedding = text_to_embedding(chosen_story['description']).reshape(1, -1)
dataset_embeddings = pd.read_pickle('books_data_embeddings.pickle')
dataset_embeddings['Similarity'] = dataset_embeddings['Description embeddings'].apply(lambda story_embedding: cosine_similarity(story_embedding.reshape(1, -1), chosen_story_embedding)[0][0]).apply(lambda x: "{:.2f}".format(x))
dataset_embeddings = dataset_embeddings.set_index('Book Name')
st.markdown("# Children Books you may like")
with st.expander("## Filters 🔎"):
    col1, col2,col3, col4 = st.columns([1,1,1,1])
    age_filter = col1.slider('Age', min_value=0, max_value=18, value=(0,18))
    price_filter = col2.slider('Price', min_value=0, max_value=100, value=(0,100))
    avg_rating_filter = col3.slider('Average Rating', min_value=1, max_value=5, value=(1,5))
    num_rating_filter = col4.slider('Number Of Rating', min_value=0, max_value=1000, value=(0,1000))

filtered_df = dataset_embeddings[
    (dataset_embeddings['min_age'] >= age_filter[0]) &
    (dataset_embeddings['max_age'] <= age_filter[1]) &
    (dataset_embeddings['Price ($)'].astype(float) >= price_filter[0]) &
    (dataset_embeddings['Price ($)'].astype(float) <= price_filter[1]) &
    (dataset_embeddings['Average Rating (Out Of 5)'].astype(float) >= avg_rating_filter[0]) &
    (dataset_embeddings['Average Rating (Out Of 5)'].astype(float) <= avg_rating_filter[1]) & 
    (dataset_embeddings['Number Of Ratings'] >= num_rating_filter[0]) &
    (dataset_embeddings['Number Of Ratings'] <= num_rating_filter[1]) 
]

filterd_df = filtered_df.sort_values('Similarity', ascending=False)
styled_dataset_embeddings = format_table(filterd_df[['Book Description', 'Age', 'Price ($)', 'Average Rating (Out Of 5)', 'Number Of Ratings']].rename(columns={'Average Rating (Out Of 5)':'Average Rating ⭐⭐⭐', 'Number Of Ratings': '#Ratings'}).head(3), cell_hover=False)
st.table(styled_dataset_embeddings)