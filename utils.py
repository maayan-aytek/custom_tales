import base64
import streamlit as st

@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

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



def init_page(logo_width=200, buttons_right="500"):
    set_background(rf'photos/background.png')
    logo_path = rf'photos\logo.png'  
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
                }}
                .stButton>button:hover {{
                    background-color: #f0f0f0;
                }}
                div.stButton > button:active {{  
                    position: relative;  
                    top: 3px;  
                }}
            </style>
            """
            ,unsafe_allow_html=True)
    img_base64 = get_base64(logo_path)
    st.markdown(f"""  
        <style>  
            .center {{  
                display: block;  
                margin-left: auto;  
                margin-right: auto; 
                margin-top: -60px;
                width: 50%;  
            }}  
                .move-left {{
            margin-left: 140px; 
        }}
        </style>  
        <img src="data:image/png;base64,{img_base64}" class="center move-left" width="{logo_width}">  
    """, unsafe_allow_html=True)

    st.markdown("""  
    <style>  
        .stTextInput input {  
            color: white;  
            height: 45px;
            border-radius: 25px;  
            backgroud-color: lightgray;
        }  
        
        .stTextInput {
            width: 250px;
            height: 100px;
            margin-left: 205px; 
            margin-bottom: -55px;
        }
    </style>  
    """, unsafe_allow_html=True)