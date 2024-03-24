import streamlit as st
import json
from google.cloud import firestore
from utils import *
import pandas as pd 
import openai
import pyttsx3
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import numpy as np
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
from multiprocessing import Pool
import soundfile as sf
import sounddevice as sd
import torch

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
set_logo(logo_width="15", top="0", right="0")
fill_color = "rgba(255, 255, 255, 0.5)"  
set_button(buttons_right="0", margin_top="200", font_size="25", height="200", color=fill_color, border_color="black")
b64_speaker_string = set_image_porperties(path=rf'photos/speaker_button_image.png', image_resize=0.19, x_padding=-17, y_padding=-9)
b64_back_string = set_image_porperties(path=rf'photos/back.png', image_resize=0.2, x_padding=-6, y_padding=-6)
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.06, x_padding=-8, y_padding=-8)


def play_wav(file_path="tts_story.wav"):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

def main():
    col1, col2, col3 = st.columns([0.05,0.05,0.8])
    with col2:
        with stylable_container(
            "home2",
            css_styles = set_image_circle_button(b64_home_string, margin_left='-80', margin_top='-70'),
        ):
            is_click_home = st.button(label='', key='button5')
            if is_click_home:
                switch_page('home')

    chosen_story = st.session_state['chosen_story']
    col21, col22 = st.columns([0.85,0.15])
    with col21:
        st.markdown(f"""        
            <div style="border: 2px solid black; padding: 10px; margin-left: -30px; border-radius: 15px; background-color: {fill_color}; color: black;">        
                <p style="font-weight: bold; font-size: 26px; text-align: center;">{chosen_story['title'].replace('*','').replace('#','')}</p>    
                <p style="font-size: 15px;">{chosen_story['story'].replace('*','').replace('#','')}</p>    
            </div>    
            """, unsafe_allow_html=True)  
        print(chosen_story['story'])
        with stylable_container(
            "speaker",
            css_styles = set_image_circle_button(b64_speaker_string, margin_left='1100', margin_top='-70'),
            ):
                is_click_speaker = st.button(label='', key='button3')
                if is_click_speaker:
                    play_wav()
    with col22:
        is_clicked_similar_books = st.button("## Similar children's books you may like :trophy:")
        if is_clicked_similar_books:
            switch_page('recommendations')
        st.image(rf'photos\giphy-unscreen.gif')

main()