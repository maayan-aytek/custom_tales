import streamlit as st
from utils import *
import pandas as pd 
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import soundfile as sf
import torch
import numpy as np

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
set_selectbox_input(width="280", margin_bottom="0", margin_left='210')
set_button(buttons_right="-245", margin_top="20")
set_tabs()
db = get_db_connection()

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
    set_logo(margin_left="600", margin_bottom="-20", logo_width=15)

user_name = st.session_state['USERNAME']
db_ref = db.collection("users").document(user_name)
doc_dict = db_ref.get().to_dict()

 
def plot_weekly_histogram(doc_dict):
    dates = []
    stories_dict = doc_dict['stories']
    for story_details in stories_dict.values():
        dates.append(datetime.strptime(story_details['generate_time'], "%d/%m/%Y"))

    last_dates_of_week = [(date + timedelta(days=(7 - date.weekday()))).strftime("%d/%m/%Y") for date in dates]
    last_dates_of_week = sorted(last_dates_of_week, reverse=True)
    fig = go.Figure(data=[go.Histogram(x=last_dates_of_week, marker=dict(color="rgb(158, 185, 243)",line=dict(width=1, color='#FFFFFF')))])

    # Set layout properties
    fig.update_layout(
        title={
            'text': "My Weekly Readings Progress",
            'y':0.9,  # Title position from top
            'x':0.5,  # Title position from left
            'xanchor': 'center',  # Anchor point for x position
            'yanchor': 'top',  # Anchor point for y position
            'font':dict(color="white")  # Set title font color to white
        },
        xaxis=dict(
            title="End Of Week",
            tickvals=last_dates_of_week,  # Set tick values to the last date of each week
            tickangle=45,  # Rotate the tick labels for better readability
            tickfont=dict(color="white"),  # Set tick font color to white
            titlefont=dict(color="white"),
            showgrid=False,
        ),
        yaxis=dict(
            title="Counts",
            tickcolor="white",  # Set tick color to white
            tickfont=dict(color="white"),  # Set tick font color to white
            titlefont=dict(color="white"), 
            showgrid=False,
        ),
        bargap=0.15,  # Gap between bars
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        paper_bgcolor="rgba(0,0,0,0)", 
        width = 500
    )

    st.plotly_chart(fig)

def plot_favorite_story_mode(doc_dict):
    modes = []
    stories_dict = doc_dict['stories']
    for story_details in stories_dict.values():
        modes.append(story_details['mode'])

    mode_counts = {mode: modes.count(mode) for mode in set(modes)}

    # Create labels and values for the pie chart
    labels = list(mode_counts.keys())
    values = list(mode_counts.values())

    # Plot the pie chart
    colors = ["rgb(158, 185, 243)", "#1F77B4", "rgb(180,151,231)"]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker = dict(
            colors=colors,
            line=dict(color='#FFFFFF', width=1)
        ))])

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",  
        legend=dict(
            x=0.73, 
            y=0.5, 
            xanchor="left",
            yanchor="middle",
            font=dict(color="white") 
        ),
        title=dict(
            text="Favorite Story Mode", 
            x=0.5, 
            y=0.9,  
            xanchor='center', 
            yanchor='top',  
            font=dict(color="white")
        ),
    )
    
    st.plotly_chart(fig)

def plot_most_frequent_morals(doc_dict, top_n=5):
    morals = []
    stories_dict = doc_dict['stories']
    for story_details in stories_dict.values():
        morals.append(story_details['moral'].lower())

    # Count the occurrences of each moral
    moral_counts = Counter(morals)

    # Get the top n most frequent morals
    top_morals = moral_counts.most_common(top_n)

    # Create lists for table data
    morals_list = [moral[0] for moral in top_morals]
    counts_list = [moral[1] for moral in top_morals]
    moral_df = pd.DataFrame({'Moral': morals_list, 'Count': counts_list})
    st.markdown(
    f"""
    <div style='margin-top: 36px;'>
        <p style='color: white; font-weight:bold;'>Top Most Frequent Morals</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    styled_dataset_embeddings = format_table(moral_df, cell_hover=False, cells_props = [('font-size', '14px'), ('text-align', 'center'), ('color', 'white')])
    st.table(styled_dataset_embeddings)
   
def restore_story(doc_dict):
    titles = []
    stories = []
    stories_dict = doc_dict['stories']
    for titel, story_details in stories_dict.items():
        titles.append(titel[1:])
        stories.append(story_details['story'][1:])

    st.markdown(
        f"""
        <div style='position: absolute; top: 10px; left: 185px;'>
            <p style='color: white; font-weight: bold;'>🔎 Search The Title To Restore The Full Story:</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_title = st.selectbox("", options=['Choose Story']+titles)
    if selected_title != 'Choose Story':
        selected_story = stories[titles.index(selected_title)]
        is_click_go_to_full_storie = st.button("Restore story")
        if is_click_go_to_full_storie:
            chosen_story = {'title':selected_title, 'story': selected_story}
            st.session_state['chosen_story'] = chosen_story
        
            with st.spinner('Loading story...'):
                device, processor, model, vocoder, speaker_embeddings = get_speaker_instances()
                
                def generate_voice(story):  
                    parts = split_text_into_parts(story)  
                    output_array = []  
                    
                    for part in parts:  
                        inputs = processor(text=part, return_tensors="pt").to(device)  
                        with torch.no_grad():  
                            generated_speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)  
                            generated_speech = generated_speech.cpu().numpy()  
                        output_array.append(generated_speech)  
                
                    speech = np.concatenate(output_array, axis=0)  
                    sf.write("tts_story.wav", speech.squeeze(), samplerate=17000)  
                
                story = chosen_story['title'] + chosen_story['story']
                generate_voice(story)

            switch_page('full_story')
            

stats_tab, restore_story_tab = st.tabs(['Statistics', 'Restore Story'])   
with stats_tab:
    col1, col2, col3, col4, col5 = st.columns([0.2, 1.6,0.8,1.1, 0.7])
    with col2:
        plot_weekly_histogram(doc_dict)
    with col3:
        plot_most_frequent_morals(doc_dict, top_n=5)
    with col4:
        plot_favorite_story_mode(doc_dict)

with restore_story_tab:
    col1, col2, col3 = st.columns([1,1,1.2])
    with col2:
     restore_story(doc_dict)