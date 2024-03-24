import base64
import streamlit as st 
import json 
import openai 
import pandas as pd

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

# @st.cache_data
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


def set_button(buttons_right, margin_top="0", font_size="18", width="200", height="50", color="white", border_color="white"):
    st.markdown(
            f"""
            <style>
                .stButton>button {{
                    font-size: {font_size}px; 
                    font-weight: bold;
                    color: black; 
                    border-width: 2px;
                    border-color: {border_color};
                    background-color: {color}; 
                    border-radius: 25px;
                    width: {width}px;
                    height: {height}px;
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


def set_logo(logo_width=50, margin_left="140", margin_bottom="-50", top=None, right=None):
    logo_path = rf'photos\logo.png'  
    img_base64 = get_base64(logo_path)
    if top and right: 
        st.markdown(f"""  
            <style>  
                .center {{  
                    display: block;  
                    width: {logo_width}%;  
                }}  
                    .move-left {{
                position: absolute;
                right: {right}px; 
                top: {top}px;
            }}
            </style>  
            <img src="data:image/png;base64,{img_base64}" class="center move-left">  
        """, unsafe_allow_html=True)
    else:
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


def set_text_input(width="250", margin_bottom="-55", margin_left='192'):
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
            margin-left: {margin_left}px; 
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


def set_selectbox_input(width="250", margin_bottom="-55", margin_left='192'):
    st.markdown(
    f"""
    <style>
    .stSelectbox {{
        margin-left: {margin_left}px; 
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


def set_image_circle_button(b64_string, margin_left='20', margin_top='20', radius='6'):
    css_style = f"""    
                    button{{
                    background-image: url("data:image/jpg;base64,{b64_string}");   
                    color: white;    
                    height: {radius}em;    
                    width: {radius}em;    
                    border-radius: 50%;    
                    border: 2px solid #BCA7E8;    
                    font-size: 8px;    
                    font-weight: bold;    
                    display: block;    
                    box-sizing: border-box;    
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.25);
                    margin-left: {margin_left}px;
                    margin-top: {margin_top}px;
                    }}"""
    return css_style
    
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
    

def split_text_into_parts(text, max_tokens=400):
    sentences = text.split(".")
    parts = []
    current_part = ""
    
    for sentence in sentences:
        if len(current_part) + len(sentence) + 1 <= max_tokens:
            current_part += sentence.strip() + "."
        else:
            parts.append(current_part.strip())
            current_part = sentence.strip() + "."
    
    if current_part:
        parts.append(current_part.strip())
    
    return parts


def format_table(df,
                 precision=None,
                 cell_hover=True,
                 cell_hover_color='#ffffb3',
                 formatter:dict =None,
                 title=None,
                 borders=True,
                 cells_props=None,
                 headers_props=None,
                 na_rep=None,
                 **kwarg):
    """Function for common dataframe styling operations"""
    fill_color = "rgba(255, 255, 255, 0.5)"  
    if isinstance(df, pd.DataFrame):
        df_style = df.style
    elif isinstance(df, pd.io.formats.style.Styler):
        df_style = df
    elif isinstance(df, pd.Series):
        df_style = df.to_frame().style
    else:
        raise TypeError(f"Wrong type! format_table() can accept ['pd.DataFrame', 'pd.io.formats.style.Styler', 'pd.Series'], got {type(df)}")

    styles = []
    #headers and index props
    if headers_props is None:
        headers_props = [('font-size', '16px'), ('text-align', 'center !important'), ('color', 'black'), ('background-color', fill_color)]
    styles.append(dict(selector="th", props=headers_props))

    #tables cells props
    if cells_props is None:
        cells_props = [('font-size', '14px'), ('text-align', 'center')]
    styles.append(dict(selector="td", props=cells_props))

    #index names props
    index_names_props = dict(selector='.index_name', props=[('font-style', 'italic')])
    styles.append(index_names_props)

    #cell hover props
    if cell_hover:  
        cell_hover_props = dict(selector="td:hover", props=[('background-color', cell_hover_color)])   
        styles.append(cell_hover_props)
        
    #table bordes props
    if borders:
        borders_style_prop = dict(selector="td, th", props=[("border", "1px solid white !important")])
        styles.append(borders_style_prop)
    
    #table title props
    if title is not None:
        title_prop = [dict(selector="caption",
                       props=[("text-align", "center"),
                              ("font-size", "150%"),
                              ("color", 'black')])]
        df_style = df_style.set_table_attributes("style='display:inline'").set_caption(title)
        styles.extend(title_prop)
    
    #set styles and foramts
    styled_df = df_style.set_table_styles(styles).format(formatter=formatter, precision=precision, na_rep=na_rep, thousands=",", **kwarg)
    return styled_df