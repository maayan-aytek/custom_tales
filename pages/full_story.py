import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import soundfile as sf
import sounddevice as sd


st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_logo(logo_width="15", top="-50", right="-60")
fill_color = "rgba(255, 255, 255, 0.5)"  
set_button(buttons_right="0", margin_top="100", font_size="25", height="200", color=fill_color, border_color="black")
b64_speaker_string = set_image_porperties(path=os.path.join('photos', 'speaker_button_image.png'), image_resize=0.19, x_padding=-17, y_padding=-9)
b64_home_string = set_image_porperties(path=os.path.join('photos', 'home_button_image.png'), image_resize=0.06, x_padding=-8, y_padding=-8)

def play_wav(file_path="tts_story.wav"):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)


def is_wav_playing():
    try:
        return sd.get_stream().active
    except:
        return False

def main():
    col1, col2, col3 = st.columns([0.05,0.05,0.8])
    with col2:
        with stylable_container(
            "home2",
            css_styles = set_image_circle_button(b64_home_string, margin_left='-130', margin_top='-80'),
        ):
            is_click_home = st.button(label='', key='button5')
            if is_click_home:
                if is_wav_playing():
                    sd.stop()
                switch_page('home')

    chosen_story = st.session_state['chosen_story']
    print(chosen_story['story'])
    col21, col22 = st.columns([0.85,0.15])
    with col21:
        st.markdown(f"""        
            <div style="border: 2px solid black; padding: 10px; margin-left: -30px; border-radius: 15px; background-color: {fill_color}; color: black;">        
                <p style="font-weight: bold; font-size: 26px; text-align: center;">{chosen_story['title'].replace('*','').replace('#','')}</p>    
                <p style="font-size: 15px;">{chosen_story['story'].replace('*','').replace('#','')}</p>    
            </div>    
            """, unsafe_allow_html=True)  
        with stylable_container(
            "speaker",
            css_styles = set_image_circle_button(b64_speaker_string, margin_left='835', margin_top='-75'),
            ):
                is_click_speaker = st.button(label='', key='button3')
                if is_click_speaker:
                    if not is_wav_playing():
                        play_wav()
                    else:
                        sd.stop()
    with col22:
        is_clicked_similar_books = st.button("## Similar children's books you may like :trophy:")
        if is_clicked_similar_books:
            if is_wav_playing():
                sd.stop()
            switch_page('recommendations')
        st.image(rf'photos\giphy-unscreen.gif')

main()