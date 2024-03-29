import streamlit as st
from utils import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                    page_title="CustomTales",
                    page_icon=os.path.join('photos', 'logo.png'))
set_background(os.path.join('photos', 'background.png'))
set_logo(logo_width=30, margin_bottom="-30", margin_left="245")
set_button(buttons_right="-250", margin_top="0")

st.markdown(" Welcome to Custom Tales! An interactive storytelling platform, where creativity meets personalization.\n")
st.write(
"""Our app leverages the power of artificial intelligence to craft customized stories tailored to your child's unique needs.\n
To get started, simply provide some basic information about your child to ensure that our stories are perfectly suited to their individuality.
 Once you've provided this information, our system works its magic to generate a story specifically designed to captivate your child's imagination. You'll have the flexibility to choose various story elements to suit your preferences.\n
 Furthermore, we understand the importance of finding the perfect children's books to nurture your child's imagination. That's why our system recommends similar children's books that align with your child's preferences, helping you make informed choices when expanding their library.\n
 In addition to personalized storytelling and insightful book recommendations, we aim to make bedtime reading more engaging, enjoyable, and memorable for families everywhere. Join us on this journey to spark imagination, foster a love of reading, and create cherished bedtime memories with your little ones.
""")
    
is_clicked_back = st.button("# Back")
if is_clicked_back:
        switch_page("main")








