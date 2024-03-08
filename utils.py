import base64
import streamlit as st

@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = """
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
    """ % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


@st.cache_resource
def get_db_connection():
    import json
    from google.cloud import firestore
    with open('config.json', 'r') as file:
        config = json.load(file)
    FIREBASE_JSON = config['FIREBASE_JSON']
    db = firestore.Client.from_service_account_json(FIREBASE_JSON)
    return db


def set_button(buttons_right, margin_top="0"):
    st.markdown(
            f"""
            <style>
                .stButton>button {{
                    font-size: 18px; 
                    font-weight: bold;
                    color: black; 
                    background-color: white; 
                    border-radius: 25px;
                    width: 200px; /* Set fixed width for the button */
                    height: 50px; /* Set fixed height for the button */
                    position: relative;  
                    right: {buttons_right}px; 
                    margin-top: {margin_top}px;
                }}
                .stButton>button:hover {{
                    background-color: #f0f0f0;
                    color: #9966ff;
                    border-color: #9966ff;
                }}
                .stButton > button:active {{  
                    background-color: #f0f0f0;
                    color: #9966ff;
                    border-color: #9966ff;
                    position: relative;  
                    top: 3px;  
                }}
            </style>
            """
            ,unsafe_allow_html=True)
    

def set_logo(logo_width=50, margin_left="140", margin_bottom="-50"):
    logo_path = rf'photos\logo.png'  
    img_base64 = get_base64(logo_path)
    st.markdown(f"""  
        <style>  
            .center {{  
                display: block;  
                margin-left: auto;  
                margin-right: auto; 
                margin-top: -60px;
                margin-bottom: {margin_bottom}px;
                width: {logo_width}%;  
            }}  
                .move-left {{
            margin-left: {margin_left}px; 
        }}
        </style>  
        <img src="data:image/png;base64,{img_base64}" class="center move-left">  
    """, unsafe_allow_html=True)


def set_text_input(width="250", margin_bottom="-55"):
    st.markdown(
    f""" 
    <style>  
        .stTextInput input {{
            color: white;  
            height: 45px;
            border-radius: 25px;  
            backgroud-color: lightgray;
        }}  
        
        .stTextInput {{
            width: {width}px;
            height: 100px;
            margin-left: 192px; 
            margin-bottom: {margin_bottom}px;
        }}
    </style>  
    """
    , unsafe_allow_html=True)


def set_number_input(width="250", margin_bottom="-55"):
    st.markdown(
    f""" 
    <style>  
        
        .stNumberInput {{
            width: {width}px;
            height: 67px;
            margin-left: 192px; 
            margin-bottom: {margin_bottom}px;
        }}
    </style>  
    """
    , unsafe_allow_html=True)


def set_selectbox_input(width="250", margin_bottom="-55"):
    st.markdown(
    f"""
    <style>
    .stSelectbox {{
        margin-left: 192px; 
        margin-bottom: {margin_bottom}px;
	}}

    .stSelectbox > div[data-baseweb="select"] > div {{
        width: {width}px;
        height: 45px;
	}}

    </style>
    """
    ,unsafe_allow_html=True)

def init_page(logo_width=200, buttons_right="500"):
    set_background(rf'photos/background.png')
    set_logo(logo_width)
    set_button(buttons_right)
    set_text_input()
    
    

    