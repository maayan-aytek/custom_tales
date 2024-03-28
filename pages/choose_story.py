import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import datetime
import numpy as np
import soundfile as sf

LEADING_CHAR = '0'

st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=f'photos/logo.png')
set_background(rf'photos/background.png')
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.06, x_padding=-8, y_padding=-8)
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
similar_story_title = st.session_state['story_details']['similar_story']
similar_story_description = st.session_state['story_details']['similar_story_description']


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

def get_response(child_age, child_gender, child_interests, story_reading_time, moral_of_the_story, mode, main_character_name, similar_story, similar_story_description):
    prompts = []
    if similar_story != "Ignored":
        similar_story_parts = [f"The story should be inspired by '{similar_story} children book. Here is the book description: {similar_story_description}.",
                            f"{similar_story}' book is the inspiration, it should echo the essence of its plot without direct replication. Here is the book description: {similar_story_description},",
                            f"{similar_story}' bookk aim to capture the story spirit and integrate it thoughtfully with a unique twist. Here is the book description: {similar_story_description}."]
    else:
        similar_story_parts = ["", "", ""]
    prompts.append(f"""Generate children story suitable for a {child_age}-year-old {child_gender} child with interests in {child_interests}. 
                    The story should be around {story_reading_time} minutes long. The moral of the story should be '{moral_of_the_story}'.
                    The mode of the story should be {mode}. The main character of the story should be named '{main_character_name}'.
                    Please note that the story doesn't have to include all interests mentioned; it can choose to include only a subset of them.
                    Also, avoid mixing unrelated interests. If there are multiple interests provided, choose at random only one that fits the story context best.
                    {similar_story_parts[0]}
                    ### Generate title: True
                    ### Generate description: True
                    ### Generate story: True
                    Your output must be in the following format: 
                    Title: ...
                    Description: ...
                    Story: ...
                    """)
    prompts.append(f"""Craft a tale for a {child_age}-year-old {child_gender} interested in {child_interests}. 
                    This narrative should unfold over approximately {story_reading_time} minutes. 
                    Central to the story is the moral '{moral_of_the_story}', which should be seamlessly woven into the plot. 
                    The narrative style is to be {mode}, and the protagonist, named '{main_character_name}', should embody the story's essence. 
                    While the story may draw from the child's interests, it should focus on a primary theme to maintain coherence. 
                    {similar_story_parts[1]}
                    ### Generate title: True
                    ### Generate description: True
                    ### Generate story: True
                    Your output must be in the following format: 
                    Title: ...
                    Description: ...
                    Story: ...
                    """)
    prompts.append(f"""Create a story appropriate for a {child_age}-year-old {child_gender}, with a spotlight on {child_interests}. 
                    The duration of the story should be close to {story_reading_time} minutes. 
                    Importantly, the storyline should impart the lesson '{moral_of_the_story}', and be presented in a {mode} manner.
                    '{main_character_name}' should lead the narrative as the principal character. While the tale can tap into various interests,
                    it should primarily revolve around one to ensure a unified theme. 
                    {similar_story_parts[2]}
                    ### Generate title: True
                    ### Generate description: True
                    ### Generate story: True
                    Your output must be in the following format: 
                    Title: ...
                    Description: ...
                    Story: ...
                    """)
    outputs = []
    for i in range(3):
        completion = openAI_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a story generator tasked with creating captivating children's stories tailored to individual preferences."},
                {"role": "user", "content": prompts[i]},
            ],
        )
        outputs.append(completion.choices[0])

    stories = []
    for choice in outputs:
        generated_content = choice.message.content
        print("-----------")
        print(generated_content)
        # Split generated content into story, title, and description
        parts = generated_content.split("Title:")
        if 'Story:' in parts[1].split("Description:")[1]:
            split_by = 'Story:'
        elif '<br/>' in parts[1].split("Description:")[1]:
            split_by = '<br/>'
        else:
            split_by = '\n\n'
        title = parts[1].split("Description:")[0].strip().replace('*', '').replace('#','')
        description = parts[1].split("Description:")[1].split(split_by)[0].strip().replace('*', '').replace('#','')
        story = parts[1].split(description)[1].replace('Story:', '').replace('*', '').replace('#','').strip()
        stories.append({'story':story, 'title':title, 'description':description})

    return stories


def change_sessison_state(name, status):
    st.session_state[name] = status


if not st.session_state['is_clicked_choose_story']:
    with st.spinner("Generating stories..."):
        stories = get_response(child_age=age, child_gender=gender, child_interests=interests, story_reading_time=reading_time, moral_of_the_story=moral,
                                mode=mode, main_character_name=main_character_name, similar_story=similar_story_title, similar_story_description=similar_story_description)
        st.session_state['stories'] = stories

if st.session_state['stories']:
    stories = st.session_state['stories']
    fill_color = "rgba(255, 255, 255, 0.5)"  
    col1, col2, col3 = st.columns([1,1,1])  
    max_height = max(len(stories[i]['title'])+len(stories[i]['description']) for i in range(3))*0.95
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

