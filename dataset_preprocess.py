from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import pandas as pd 
import torch


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
model = AutoModel.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def text_to_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    
    if 'overflowing_tokens' in inputs:
        print(f"Warning: Input sequence length exceeded maximum length. Truncating sequence for text: {text}")
    
    inputs.to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    
    sentence_embeddings = mean_pooling(outputs, inputs['attention_mask'])
    return sentence_embeddings.cpu().numpy()

dataset = pd.read_csv('books_data.csv')
dataset = dataset.dropna(subset=['Name', 'Description','Age', 'Price', 'Rating_out_of_5' , 'No_of_Ratings'])
dataset = dataset.rename(columns={'Name':'Book Name',
                                  'Description':'Book Description',
                                  'Price':'Price ($)',
                                  'Rating_out_of_5':'Average Rating (Out Of 5)',
                                  'No_of_Ratings':'Number Of Ratings'})
dataset['Price ($)'] = dataset['Price ($)'].str.replace('$','').str.strip().astype(float).apply(lambda x: "{:.2f}".format(x))
dataset['Number Of Ratings'] = dataset['Number Of Ratings'].astype(int)
dataset['Average Rating (Out Of 5)'] = dataset['Average Rating (Out Of 5)'].astype(float).apply(lambda x: "{:.2f}".format(x))
dataset['Age'] =  dataset['Age'].str.replace("Great On Kindle: A high quality digital reading experience.", "")
dataset['Age'] =  dataset['Age'].str.replace("Ages: ", "")
dataset = dataset[dataset["Book Name"] != "The Magic of Manifesting: 15 Advanced Techniques To Attract Your Best Life, Even If You Think It's Impossible Now"]
def extract_age_range(age_str):
    if 'years and up' in age_str or 'year and up' in age_str:
        min_age = int(age_str.split()[0])
        max_age = 100
    else:
        min_age, max_age = age_str.replace(' years', '').split(' - ')
    return int(min_age), int(max_age)
dataset[['min_age', 'max_age']] = dataset['Age'].apply(lambda x: pd.Series(extract_age_range(x)))

embedding = []
for i, text in enumerate(dataset['Book Description']):
    print(i)
    embedding.append(text_to_embedding(text))
dataset['Description embeddings'] = embedding
dataset.to_pickle('books_data_embeddings.pickle')

dataset = pd.read_pickle('books_data_embeddings.pickle')