import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_data = pd.read_csv('./movies.csv')

movies_data.head()

movies_data.shape

selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', ]

for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')
combined_features = movies_data['genres']+' '+movies_data['keywords']+' ' + \
    movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']
vectorizer = TfidfVectorizer()

feature_vectors = vectorizer.fit_transform(combined_features)
similarity = cosine_similarity(feature_vectors)


def findmovie(movie_name):

    list_of_all_titles = movies_data['title'].tolist()
    iroclose_match = difflib.get_close_matches(
        movie_name, list_of_all_titles)[0]
    index_of_the_movie = movies_data[movies_data.title == iroclose_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    i = 1
    txt = []
    for movies in sorted_similar_movies:
        title_from_the_index = movies_data[movies_data.index == movies[0]]['title'].values[0]
        if (i < 21):
            
            txt.append(title_from_the_index)
            i += 1
        if (i > 4803):
            return "ERROR: Movie not found :("
    return txt

