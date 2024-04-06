<h1 align="center" id="title">CustomTales</h1>

<p id="description">Welcome to Custom Tales! An interactive storytelling streamlit app where creativity meets personalization. Our app leverages the power of artificial intelligence to craft customized stories tailored to your child's unique needs. Furthermore our system recommends similar children's books that align with your child's preferences helping you make informed choices when expanding their library.</p> 
<p>To get started follow the link to our app: https://customtales.streamlit.app/ </p>

<img src="https://github.com/maayan-aytek/custom_tales/assets/81248290/878fbd3b-c6a1-4666-94dc-ce766516afef" width="250" align="center"/>

<h2>🛠️ Installation Steps:</h2>

<p id="description">You don't have to run our app local. You can simply use our public link. However, if you want to utilize a GPU (if you have one) to speed up preformance, you can run it locally by following these steps:</p>
<p>1. Create conda environment</p>

```
conda create --name myenv --file requirements.txt
```

<p>2. Activate the environment</p>

```
conda activate myenv
```

<p>3. Add your firebase firestore-key json to the main folder</p>

<p>4. Create an OpenAI API key</p>

<p>5. Edit config.json with you own keys:</p>

```
{
    "OPENAI_KEY": "key",
    "FIREBASE_JSON": "database key"
}
```

<p>6. Edit utils.py get_openAI_client() function by uncommenting the commented out lines and comment out the first line. Your function should look like this:</p>

```
def get_openAI_client():
    # OPENAI_KEY = st.secrets['OPENAI_KEY']
    with open('config.json', 'r') as file:
         config = json.load(file)
    OPENAI_KEY = config['OPENAI_KEY']
    openai.api_key = OPENAI_KEY
    client = openai.OpenAI(api_key=OPENAI_KEY)
    return client
```

<p>7. Edit utils.py get_db_connection() function by adding your firebase json file path (from step 3) and removing the st.secrets. Your function should look like this: f:</p>

```
def get_db_connection():
    import json
    from google.cloud import firestore
    # FIREBASE_JSON = "customtales-b1c5d-firebase-adminsdk-c7ntb-7689c30bb8.json"
    LOCAL_PATH = "the path to your file"
    # with open(FIREBASE_JSON, 'r') as file:
    #     config = json.load(file)
    # config["private_key_id"] = st.secrets["private_key_id"]
    # config["private_key"] = st.secrets["private_key"]
    # config["client_email"] = st.secrets["client_email"]
    # config["client_id"] = st.secrets["client_id"]
    # config["client_x509_cert_url"] = st.secrets["client_x509_cert_url"]
    
    # with open(FIREBASE_JSON, 'w') as file:
    #     json.dump(config, file)

    db = firestore.Client.from_service_account_json(LOCAL_PATH)
    return db
```

<p>8. Run the app</p>

```
streamlit run main.py
```
