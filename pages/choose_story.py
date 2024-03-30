import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import datetime
import numpy as np
import soundfile as sf
from multiprocessing import Pool  

LEADING_CHAR = '0'

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
b64_home_string = set_image_porperties(os.path.join('photos', 'home_button_image.png'), image_resize=0.06, x_padding=-8, y_padding=-8)

db = get_db_connection()
device, processor, model, vocoder, speaker_embeddings = get_speaker_instances()

col01, col02, col03 = st.columns([0.05,0.05,0.8])
with col02:
    with stylable_container(
        "home",
        css_styles = set_image_circle_button(b64_home_string, margin_left='-270', margin_top='-60'),
    ):
        is_click_home = st.button(label='', key='button2')
        if is_click_home:
            switch_page('home')
with col03:
    set_logo(logo_width="15", margin_left="335", margin_bottom="0")
set_circle_button()


def worker(part):
    print(part)
    inputs = processor(text=part, return_tensors="pt").to(device)  
    with torch.no_grad():  
        generated_speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)  
        generated_speech = generated_speech.cpu().numpy() 
    print("finish", part)
    return generated_speech


def generate_voice(story):  
    print("start")
    parts = split_text_into_parts(story)  
    print("after split")
    output_array = []
    device = "cpu"
    if device=="cuda":
        for part in parts:  
            generated_speech = worker(part)
            output_array.append(generated_speech)  
    else:
        print("here")
        with Pool() as pool:  
            # Use the Pool's map function to apply string_to_array to each string.  
            arrays = pool.map(worker, parts)  
        output_array = arrays

    speech = np.concatenate(output_array, axis=0)  
    sf.write("tts_story.wav", speech.squeeze(), samplerate=17000)
    print(speech)


def update_story(chosen_story):
    st.session_state['chosen_story'] = chosen_story
    chosen_story = {key: LEADING_CHAR + value for key, value in chosen_story.items()}
    title = chosen_story['title']
    doc_ref = db.collection("users").document(st.session_state['USERNAME'])
    doc = doc_ref.get()
    chosen_story['generate_time'] = datetime.date.today().strftime("%d/%m/%Y")
    chosen_story.update(st.session_state['story_details'])
    if not doc.exists or 'stories' not in doc.to_dict():
        doc_ref.update({
            "stories": {title: chosen_story}
        })
    else:
        doc_ref.update({
            f"stories.{title}": chosen_story,
        })

    with st.spinner('Loading story...'):       
        story = chosen_story['title'] + chosen_story['story']
        generate_voice(story)
        
    switch_page('full_story')


def change_sessison_state(arg_name, status):
    st.session_state[arg_name] = status


if __name__ == "__main__":
    if st.session_state['is_story_1_clicked']:
        st.session_state['is_clicked_choose_story'] = True
        st.session_state['is_story_1_clicked'] = False
        stories = st.session_state['stories']
        update_story(stories[0])
    if st.session_state['is_story_2_clicked']:
        st.session_state['is_clicked_choose_story'] = True
        st.session_state['is_story_2_clicked'] = False
        stories = st.session_state['stories']
        update_story(stories[1])
    if st.session_state['is_story_3_clicked']:
        st.session_state['is_clicked_choose_story'] = True
        st.session_state['is_story_3_clicked'] = False
        stories = st.session_state['stories']
        update_story(stories[2])

    if st.session_state['stories']:
        stories = st.session_state['stories']
        fill_color = "rgba(255, 255, 255, 0.5)"  
        col1, col2, col3 = st.columns([1,1,1])
        long_title = False
        for i in range(3):
            title_len = len(stories[i]['title'])
            if title_len > 26:
                long_title = True

        height_ratio = 1.1 if long_title else 1
        max_height = max(len(stories[i]['title'])+len(stories[i]['description']) for i in range(3))*height_ratio
        with col1:  
            st.markdown(f"""        
                <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 15px; background-color: {fill_color}; color: black; height: {max_height}px;">        
                    <p style="font-weight: bold; font-size: 26px; text-align: center;">{stories[0]['title'].replace('**','').replace('#','')}</p>    
                    <p style="font-size: 15px;">{stories[0]['description'].replace('*','').replace('#','')}</p>    
                </div>    
                """, unsafe_allow_html=True)   
            is_story_1_clicked = st.button("1", on_click=change_sessison_state, args=['is_story_1_clicked', True])

        with col2:  
            st.markdown(f"""        
                <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 15px; background-color: {fill_color}; color: black; height: {max_height}px;">        
                    <p style="font-weight: bold; font-size: 26px; text-align: center;">{stories[1]['title'].replace('**','').replace('#','')}</p>    
                    <p style="font-size: 15px;">{stories[1]['description'].replace('*','').replace('#','')}</p>    
                </div>    
                """, unsafe_allow_html=True)   
            is_story_2_clicked = st.button("2", on_click=change_sessison_state, args=['is_story_2_clicked', True])
            
        with col3:  
            st.markdown(f"""        
                <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 15px; background-color: {fill_color}; color: black; height: {max_height}px;">        
                    <p style="font-weight: bold; font-size: 26px; text-align: center;">{stories[2]['title'].replace('**','').replace('###','')}</p>    
                    <p style="font-size: 15px; color: black;">{stories[2]['description'].replace('*','').replace('#','')}</p>  
                </div>    
                """, unsafe_allow_html=True)    
            is_story_3_clicked = st.button("3", on_click=change_sessison_state, args=['is_story_3_clicked', True]) 