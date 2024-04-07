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


# page and styling configurations 
st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_selectbox_input(width="280", margin_left='30', margin_top=-20)
set_button(margin_top=60, buttons_right=-70)
set_tabs()
db = get_db_connection()

# Setting home button
b64_home_string = set_image_porperties(os.path.join('photos', 'home_button_image.png'), image_resize=0.06, x_padding=-8, y_padding=-8)
col1, col2, col3 = st.columns([0.05,0.05,0.8])
with col2:
    with stylable_container(
        "home",
        css_styles = set_image_circle_button(b64_home_string, margin_left='-200', margin_top='-95'),
    ):
        is_click_home = st.button(label='', key='button2')
        if is_click_home:
            switch_page('home')
with col3:
    set_logo(right=-60, top=-100, margin_bottom="-80", logo_width=15)


# Getting the user information from the database for statistics calculations 
user_name = st.session_state['USERNAME']
db_ref = db.collection("users").document(user_name)
doc_dict = db_ref.get().to_dict()

 
 # Plot the user's weekly reading progress
def plot_weekly_histogram(doc_dict):
    dates = []
    stories_dict = doc_dict['stories']
    for story_details in stories_dict.values():
        dates.append(datetime.strptime(story_details['generate_time'], "%d/%m/%Y"))

    last_dates_of_week = [(date + timedelta(days=(7 - date.weekday()))).strftime("%d/%m/%Y") for date in dates]
    last_dates_of_week = [datetime.strptime(date, "%d/%m/%Y") for date in last_dates_of_week]
    last_dates_of_week = sorted(last_dates_of_week, reverse=True)
    fig = go.Figure(data=[go.Histogram(x=last_dates_of_week, marker=dict(color="rgb(158, 185, 243)",line=dict(width=1, color='#FFFFFF')))])

    # Set layout properties
    fig.update_layout(
        title={
            'text': "My Weekly Readings Progress",
            'y':0.9,
            'x':0.5,  
            'xanchor': 'center', 
            'yanchor': 'top', 
            'font':dict(color="white")
        },
        xaxis=dict(
            title="End Of Week",
            tickvals=last_dates_of_week,
            tickangle=45,
            tickfont=dict(color="white"), 
            titlefont=dict(color="white"),
            showgrid=False,
        ),
        yaxis=dict(
            title="Counts",
            tickcolor="white",  
            tickfont=dict(color="white"), 
            titlefont=dict(color="white"), 
            showgrid=False,
        ),
        bargap=0.15,  # Gap between bars
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        paper_bgcolor="rgba(0,0,0,0)", 
        width = 300
    )

    st.plotly_chart(fig)


 # Plot the user's favorite story modes pie
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
            xanchor="left",
            yanchor="middle",
            font=dict(color="white") 
        ),
        title=dict(
            text="Favorite Story Mode", 
            x=0.4, 
            y=0.9,  
            xanchor='center', 
            yanchor='top',  
            font=dict(color="white")
        ),
        width=400
    )
    
    st.plotly_chart(fig)


 # Plot the user's most frequent morals as a table
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
    moral_df.index += 1
    st.markdown(
    f"""
    <div style='margin-top: 36px; text-align: center'>
        <p style='color: white; font-weight:bold;'>Top {top_n} Most Frequent Morals</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    st.write('')
    st.write('')
    styled_dataset_embeddings = format_table(moral_df, cell_hover=False, cells_props = [('font-size', '14px'), ('text-align', 'center'), ('color', 'white')])
    st.table(styled_dataset_embeddings)
   

# Restore existing story. By clicking on the story title the user will be moved to 'full story' page.
def restore_story(doc_dict):
    titles = []
    stories = []
    stories_dict = doc_dict['stories']
    for titel, story_details in stories_dict.items():
        titles.append(titel[1:])
        stories.append(story_details['story'][1:])

    st.markdown(
        f"""
        <div >
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
        

            # Loading the restores story audio file
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
            

# Styling
stats_tab, restore_story_tab = st.tabs(['Statistics', 'Restore Story'])   
with stats_tab:
    col1, col2, col3 = st.columns([0.7, 1.2, 1.1])
    with col1:
        plot_weekly_histogram(doc_dict)
    with col2:
        plot_most_frequent_morals(doc_dict, top_n=5)
    with col3:
        plot_favorite_story_mode(doc_dict)

with restore_story_tab:
    col1, col2, col3 = st.columns([1,1,1.2])
    with col2:
        restore_story(doc_dict)