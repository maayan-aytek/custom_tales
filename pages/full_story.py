import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
import soundfile as sf
import pickle 


# page and styling configurations 
st.set_page_config(layout="wide",
                   initial_sidebar_state="collapsed",
                   page_title="CustomTales",
                   page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_logo(logo_width="15", top="-50", right="-40")
set_multiSelectBox_input()
set_selectbox_input(width="400", margin_left='-20')
fill_color = "rgba(255, 255, 255, 0.5)"
set_button(buttons_right="-40", margin_top="120", font_size="25", height="200", color=fill_color, border_color="black")
b64_speaker_string = set_image_porperties(path=os.path.join('photos', 'speaker_button_image.png'), image_resize=0.19,
                                          x_padding=-17, y_padding=-9)
b64_home_string = set_image_porperties(path=os.path.join('photos', 'home_button_image.png'), image_resize=0.06,
                                       x_padding=-8, y_padding=-8)

openAI_client = get_openAI_client()
db = get_db_connection()

# Loading tokenizer model for splitting text by sentences
with open('punkt.pickle', 'rb') as f:
        tokenizer = pickle.load(f)

# Playing the story audio file 
def play_wav(file_path="tts_story.wav"):
    data, samplerate = sf.read(file_path)
    st.audio(data, format="audio/wav", sample_rate=samplerate)


# Numbering the rows in the full story (for the editing part)
def add_row_number(story):
  sentences = tokenizer.tokenize(story)
  sentences_dict = {(i+1):sen for i, sen in enumerate(sentences)}
  for i, sen in sentences_dict.items():
    index = story.find(sen)
    prefix = story[:index]
    suffix = story[index:]
    story = prefix + f'({i}) ' + suffix
  return story, sentences_dict


# Edit story by the selected rows numbers 
def replace_sentences(row_number_2_change, reason_to_change, sentences_dict):
    # Mapping the reason string to the prompt for the LLM
    reason_dict = {"Not to My Taste": "I want to change these lines because it doesn't match my preferences.", 
                   "Uninspiring": "These lines lack creativity for me; I'd like to inject more inspiration into it.", 
                   "Feels Forced": "These lines feels unnatural; I'd prefer something that flows more organically.", 
                   "Needs Improvement":  "I believe these lines could be better crafted to convey the intended message or scene.",
                   "Disrupts Flow": "I find that these lines disrupts the narrative flow; I'd like to make it smoother.", 
                   "Other": "Change these lines to something else"}
    
    # Building prompt for editing the story
    initial_story = st.session_state['chosen_story']['story'].replace('*','').replace('#','')
    sentences2prompt = [f"- {sentences_dict[i_sen]}\n" for i_sen in row_number_2_change]
    prompt = f"""Below is the story you generated,
      along with a list of specific lines I'd like to alter and the reasons for each change. Your task is to use this information
        to regenerate the story with the requested modifications. I am going to give you the Original generated story, the lines to change and the reason for changes and you will return the modified story with the changes in the lines I asked.
        **Original Generated Story:**
        {initial_story}

        **Lines to Change:**
        {"".join(sentences2prompt)}

        **Reason for Changes:**
        {reason_dict[reason_to_change]}

        **Instructions:**
        - Only modify the lines provided in the 'Lines to Change' section; do not alter any other lines in the story.
        - Ensure that the modifications align with the specified reasons for each line change.
        - Maintain coherence and consistency in the narrative while incorporating the requested alterations.
        - Output the revised story with the changes.
        """
    
    completion = openAI_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a story generator tasked with creating captivating children's stories tailored to individual preferences."},
            {"role": "user", "content": prompt},
        ],
    )
    story_after_change = completion.choices[0].message.content
    # update the edited story in the session_state
    st.session_state['chosen_story']['story'] = story_after_change.split(":**\n")[1]
    title = st.session_state['chosen_story']['title']

    # Update the edited story in the database
    doc_ref = db.collection("users").document(st.session_state['USERNAME'])
    doc_ref.update({f"stories.{LEADING_CHAR + title}.story": LEADING_CHAR + story_after_change})



def main():
    # Styling 
    _, col2, _ = st.columns([0.05, 0.05, 0.8])
    with col2:
        with stylable_container(
                "home2",
                css_styles=set_image_circle_button(b64_home_string, margin_left='-170', margin_top='-80'),
        ):
            is_click_home = st.button(label='', key='button5')
            if is_click_home:
                switch_page('home')

    
    chosen_story = st.session_state['chosen_story']
    col21, col22 = st.columns([0.85, 0.15])
    with col21:
        story, sentences_dict = add_row_number(chosen_story['story'].replace('*','').replace('#',''))
        st.markdown(f"""
            <div style="border: 2px solid black; padding: 10px; margin-left: -30px; border-radius: 15px; background-color: {fill_color}; color: black;">
                <p style="font-weight: bold; font-size: 26px; text-align: center;">{chosen_story['title'].replace('*','').replace('#','')}</p>
                <p style="font-size: 15px;">{story}</p>
            </div>
            """, unsafe_allow_html=True)
        with stylable_container(
                "speaker",
                css_styles=set_image_circle_button(b64_speaker_string, margin_left='1060', margin_top='-72'),
        ):
            is_click_speaker = st.button(label='', key='button3')
            if is_click_speaker:
                play_wav()

    with col22:
        is_clicked_similar_books = st.button("## Similar children's books you may like :trophy:")
        if is_clicked_similar_books:
            switch_page('recommendations')
        st.image(os.path.join('photos', 'giphy-unscreen.gif'))

    # Editing interation styling
    row_number_2_change = st.multiselect('Select the lines numbers that you want to modify.', options=list(sentences_dict.keys()), help='')
    if row_number_2_change != []:
        reason_to_change = st.selectbox("Explain why do you want to modify these lines:",options=['Not to My Taste', 'Feel Forced', 'Uninspiring', 'Disrupts Flow', 'Needs Improvement', 'Other'])
        if reason_to_change != '':
            with stylable_container(
                "home",
                css_styles = set_custom_button(),
            ):
                is_click_replace_sen = st.button('Replace!')
                if is_click_replace_sen:
                    with st.spinner("Editing your story..."): 
                        replace_sentences(row_number_2_change, reason_to_change, sentences_dict)
                        # Load the page again with the edited story
                        st.rerun()

main()
