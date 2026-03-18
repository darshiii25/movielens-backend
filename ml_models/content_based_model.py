import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("datasets/tmdb_5000_movies.csv")
credits = pd.read_csv("datasets/tmdb_5000_credits.csv")

movie = movies.merge(credits, on='title')
movie = movie[['movie_id','title','overview','genres','keywords','cast','crew']]
movie.dropna(inplace=True)

def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert2(obj):
    L=[]
    count=0
    for i in ast.literal_eval(obj):
        if count<3:
            L.append(i['name'])
            count+=1
        else:
            break
    return L

def convert3(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
            break
    return L

movie['genres'] = movie['genres'].apply(convert)
movie['keywords'] = movie['keywords'].apply(convert)
movie['cast'] = movie['cast'].apply(convert2)
movie['crew'] = movie['crew'].apply(convert3)

movie['overview'] = movie['overview'].apply(lambda x: x.split())

movie['genres'] = movie['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movie['keywords'] = movie['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movie['cast'] = movie['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movie['crew'] = movie['crew'].apply(lambda x:[i.replace(" ","") for i in x])

movie['tag'] = movie['overview'] + movie['genres'] + movie['keywords'] + movie['cast'] + movie['crew']

new_df = movie[['movie_id','title','tag']]

new_df['tag'] = new_df['tag'].apply(lambda x:" ".join(x))
new_df['tag'] = new_df['tag'].apply(lambda x:x.lower())

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tag']).toarray()

similarity = cosine_similarity(vectors)

def content_recommend(movie_name):

    print("INPUT:", movie_name)

    # ✅ Step 1: lowercase conversion
    movie_name = movie_name.lower()
    new_df['title'] = new_df['title'].str.lower()

    if movie_name not in new_df['title'].values:
        print("NOT FOUND")
        return ["Movie not found in dataset"]

    index = new_df[new_df['title'] == movie_name].index[0]

    print("INDEX:", index)

    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)

    recommended_movies = []

    for i in distances[1:6]:
        recommended_movies.append(new_df.iloc[i[0]].title)

    print("OUTPUT:", recommended_movies)

    return recommended_movies