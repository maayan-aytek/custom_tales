import base64
import streamlit as st 
import json 
import openai 

@st.cache_resource
def get_openAI_client():
    with open('config.json', 'r') as file:
        config = json.load(file)

    OPENAI_KEY = config['OPENAI_KEY']
    openai.api_key = OPENAI_KEY
    client = openai.OpenAI(api_key=OPENAI_KEY)
    return client

@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache_data
def set_image_porperties(path="photos/generate_story_image.png", image_resize=0.1, x_padding=-12, y_padding=-12):
    import base64  
    from PIL import Image  
    import io 
    with Image.open(path) as img:  
        # Resize the image
        width, height = img.size   
        resized_img = img.resize((int(width * image_resize), int(height * image_resize)))  
        x, y = resized_img.size  
        new_img = Image.new('RGB', (x, y), 'white') 
        new_img.paste(resized_img, (x_padding, y_padding)) 
    
    # Convert the image to bytes  
    img_byte_arr = io.BytesIO()  
    new_img.save(img_byte_arr, format='PNG')  
    img_byte_arr = img_byte_arr.getvalue()  
    
    # Convert the bytes to base64 string  
    b64_string = base64.b64encode(img_byte_arr).decode("utf-8")  
    return b64_string


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
    
def set_help_tooltip(margin_left='100'):
    st.markdown(  
    f"""  
    <style>  
    .stTooltip {{  
        margin-left: {margin_left}px;  
    }}  
    </style>  
    """,  
    unsafe_allow_html=True)  


def set_image_circle_button(b64_string, margin_left='20'):
    st.markdown(f"""    
            <style>    
                div.stButton > button:first-child {{    
                    background-image: url("data:image/jpg;base64,{b64_string}");   
                    color: white;    
                    height: 10em;    
                    width: 10em;    
                    border-radius: 50%;    
                    border: 2px solid #BCA7E8;    
                    font-size: 8px;    
                    font-weight: bold;    
                    display: block;    
                    box-sizing: border-box;    
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.25);
                    margin-left: {margin_left}px;
                }}    
        
                div.stButton > button:hover {{  
                    border: 2px solid #6A0DAD; 
                }}  
        
                div.stButton > {{
                    position: relative;    
                    top: 3px; 
                }}  
    
            </style>    
        """, unsafe_allow_html=True) 
    
def set_circle_button(margin_left='100'):    
    st.markdown(f"""        
            <style>        
                div.stButton > button:first-child {{        
                    background-color: rgba(255, 255, 255, 0.5);       
                    color: purple;        
                    height: 5em;        
                    width: 5em;        
                    border-radius: 50%;        
                    border: 2px solid #BCA7E8;        
                    font-size: 12px;     
                    line-height: 1em;  
                    box-sizing: border-box;        
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.25);  
                }}        
  
                div.stButton > button:hover {{      
                    border: 2px solid #6A0DAD;     
                }}   
  
                div.stButton {{        
                    display: flex;        
                    justify-content: center;        
                    align-items: center;   
                }}      
            </style>        
        """, unsafe_allow_html=True)    
    