import streamlit as st
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
openAI_client = get_openAI_client()

b64_gen_story_string = set_image_porperties(path=rf'photos/generate_story_image.png', image_resize=0.105, x_padding=-10, y_padding=-13)
b64_home_string = set_image_porperties(path=rf'photos/home_button_image.png', image_resize=0.06, x_padding=-8, y_padding=-8)

col1, col2, col3 = st.columns([0.05,0.05,0.8])
with col2:
    with stylable_container(
        "home",
        css_styles = set_image_circle_button(b64_home_string, margin_left='-280', margin_top='-75'),
    ):
        is_click_home = st.button(label='', key='button2')
        if is_click_home:
            switch_page('home')
with col3:
    set_logo(margin_bottom="-80", logo_width=20, top=-80, right=-240)



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
moral = st.text_input("Moral", help="""Examples:\n1. Be kind\n2. Believe in yourself\n3. Be Grateful for What You Have\n4. Never Judge a Book by its Cover\n5. Honesty is the Best Policy\n6. You only live once\n7. Never give up""")
mode = st.selectbox("Mode", options=["Classic", "Creative", "Innovative"], placeholder="")
main_character_name = st.text_input("Main Character Name", placeholder="", help="If not provided, the main character name will default to the child's name.")
similar_story = st.selectbox("Story Inspiration", options=['Ignored'] + list(books_df['Name'].drop_duplicates().sort_values()), help="""Select the story template or framework to use as a basis when creating a new story.\n\nIf you're unsure which template to choose, you can leave this field as 'ignored', and a new story will be created from scratch.""")
similar_story_description = "" if similar_story == "Ignored" else books_df[books_df['Name'] == similar_story]['Description'].values[0]

with stylable_container(
    "generate_story",
    css_styles = set_image_circle_button(b64_gen_story_string, radius='11', margin_left='300'),
):
    is_click_generate_story = st.button(label='',key="story_time - generate_story")

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


if is_click_generate_story:
    if is_validate_details(reading_time, moral, mode):
        st.session_state['story_details'] = {'reading_time': reading_time,
                                            'moral': moral,
                                            'mode': mode,
                                            'main_character_name': st.session_state['NAME'] if main_character_name == '' else main_character_name,
                                            'similar_story': similar_story,
                                            'similar_story_description': similar_story_description
                                            }
        st.session_state['is_story_1_clicked'] = False
        st.session_state['is_story_2_clicked'] = False
        st.session_state['is_story_3_clicked'] = False
        st.session_state['is_clicked_choose_story'] = False
        st.session_state['stories'] = None

        with st.spinner("Generating stories..."):
            name = st.session_state['NAME']
            age = st.session_state['AGE']
            gender = st.session_state['GENDER']
            interests = st.session_state['INTERESTS']
            similar_story_title = st.session_state['story_details']['similar_story']
            similar_story_description = st.session_state['story_details']['similar_story_description']
            stories = get_response(child_age=age, child_gender=gender, child_interests=interests, story_reading_time=reading_time, moral_of_the_story=moral,
                                    mode=mode, main_character_name=main_character_name, similar_story=similar_story_title, similar_story_description=similar_story_description)
            st.session_state['stories'] = stories
        switch_page("choose_story")

        

