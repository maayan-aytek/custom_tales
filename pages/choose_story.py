import streamlit as st
import json
from google.cloud import firestore
from utils import *
import pandas as pd 
import openai
from streamlit_extras.switch_page_button import switch_page
import pickle

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
set_logo(logo_width="15", margin_left="455", margin_bottom="0")
set_circle_button()

openAI_client = get_openAI_client()
db = get_db_connection()

name = st.session_state['NAME']
age = st.session_state['AGE']
gender = st.session_state['GENDER']
interests = st.session_state['INTERESTS']

reading_time = st.session_state['story_details']['reading_time']
moral = st.session_state['story_details']['moral']
mode = st.session_state['story_details']['mode']
main_character_name = st.session_state['story_details']['main_character_name']
similar_story = st.session_state['story_details']['similar_story']


def get_response(child_age, child_gender, child_interests, story_reading_time, moral_of_the_story, mode, main_character_name):
    prompt = f"""Generate children story suitable for a {child_age}-year-old {child_gender} child with interests in {child_interests}. 
                The story should be around {story_reading_time} minutes long. The moral of the story should be '{moral_of_the_story}'.
                The mode of the story should be {mode}. The main character of the story should be named '{main_character_name}'.
                Please note that the story doesn't have to include all interests mentioned; it can choose to include only a subset of them.
                Also, avoid mixing unrelated interests. If there are multiple interests provided, choose at random only one that fits the story context best.
                ### Generate title: True
                ### Generate description: True
                ### Generate story: True
                """
    completion = openAI_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a story generator tasked with creating captivating children's stories tailored to individual preferences."},
            {"role": "user", "content": prompt},
            # {"role": "assiatance", "content": prompt_with_assistance},
        ],
        n=3
    )

    stories = []
    for choice in completion.choices:
        generated_content = choice.message.content
        # Split generated content into story, title, and description
        parts = generated_content.split("Title:")
        title = parts[1].split("Description:")[0].strip().replace('**', '').replace('###','')
        description = parts[1].split("Description:")[1].split("Story:")[0].strip().replace('**', '').replace('###','')
        story = parts[1].split("Description:")[1].split("Story:")[1].strip().replace('**', '').replace('###','')
        stories.append({'story':story, 'title':title, 'description':description})

    return stories


# stories = get_response(child_age=age, child_gender=gender, child_interests=interests, story_reading_time=reading_time, moral_of_the_story=moral, mode=mode, main_character_name=main_character_name)
with open('stories.pickle', 'rb') as file:
    stories = pickle.load(file)


fill_color = "rgba(255, 255, 255, 0.5)"  
col1, col2, col3 = st.columns([1,1,1])  
max_height = max(len(stories[i]['title'])+len(stories[i]['description']) for i in range(3))*0.9
with col1:  
    st.markdown(f"""        
        <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 15px; background-color: {fill_color}; color: black; height: {max_height}px;">        
            <p style="font-weight: bold; font-size: 26px; text-align: center;">{stories[0]['title'].replace('**','').replace('###','')}</p>    
            <p style="font-size: 15px;">{stories[0]['description'].replace('**','').replace('###','')}</p>    
        </div>    
        """, unsafe_allow_html=True)   
    is_story_1_clicked = st.button("1")  
with col2:  
    st.markdown(f"""        
        <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 15px; background-color: {fill_color}; color: black; height: {max_height}px;">        
            <p style="font-weight: bold; font-size: 26px; text-align: center;">{stories[1]['title'].replace('**','').replace('###','')}</p>    
            <p style="font-size: 15px;">{stories[1]['description'].replace('**','').replace('###','')}</p>    
        </div>    
        """, unsafe_allow_html=True)   
    is_story_2_clicked = st.button("2")  
with col3:  
    st.markdown(f"""        
        <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 15px; background-color: {fill_color}; color: black; height: {max_height}px;">        
            <p style="font-weight: bold; font-size: 26px; text-align: center;">{stories[2]['title'].replace('**','').replace('###','')}</p>    
            <p style="font-size: 15px; color: black;">{stories[2]['description'].replace('**','').replace('###','')}</p>  
        </div>    
        """, unsafe_allow_html=True)    
    is_story_3_clicked = st.button("3") 


if is_story_1_clicked:
    pass
if is_story_2_clicked:
    pass
if is_story_3_clicked:
    pass