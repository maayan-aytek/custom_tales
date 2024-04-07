import pandas as pd 
from utils import text_to_embedding


def extract_age_range(age_str):
    if 'years and up' in age_str or 'year and up' in age_str:
        min_age = int(age_str.split()[0])
        max_age = 100
    else:
        min_age, max_age = age_str.replace(' years', '').split(' - ')
    return int(min_age), int(max_age)


# Pre processing on the books dataset
dataset = pd.read_csv('books_data.csv')
# remove nulls
dataset = dataset.dropna(subset=['Name', 'Description','Age', 'Price', 'Rating_out_of_5' , 'No_of_Ratings']) 
# rename columns 
dataset = dataset.rename(columns={'Name':'Book Name',
                                  'Description':'Book Description',
                                  'Price':'Price ($)',
                                  'Rating_out_of_5':'Average Rating (Out Of 5)',
                                  'No_of_Ratings':'Number Of Ratings'})
# align columns to single format
dataset['Price ($)'] = dataset['Price ($)'].str.replace('$','').str.strip().astype(float).apply(lambda x: "{:.2f}".format(x))
dataset['Number Of Ratings'] = dataset['Number Of Ratings'].astype(int)
dataset['Average Rating (Out Of 5)'] = dataset['Average Rating (Out Of 5)'].astype(float).apply(lambda x: "{:.2f}".format(x))
dataset['Age'] =  dataset['Age'].str.replace("Great On Kindle: A high quality digital reading experience.", "")
dataset['Age'] =  dataset['Age'].str.replace("Ages: ", "")
# removing outliers 
dataset = dataset[dataset["Book Name"] != "The Magic of Manifesting: 15 Advanced Techniques To Attract Your Best Life, Even If You Think It's Impossible Now"]

# adding min and max age columns
dataset[['min_age', 'max_age']] = dataset['Age'].apply(lambda x: pd.Series(extract_age_range(x)))


# represent book description as embedding
embedding = []
for i, text in enumerate(dataset['Book Description']):
    embedding.append(text_to_embedding(text))
dataset['Description embeddings'] = embedding

# saving to pickle
dataset.to_pickle('books_data_embeddings.pickle')