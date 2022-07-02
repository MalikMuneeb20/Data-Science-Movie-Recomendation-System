import os


from distutils.spawn import find_executable
os.system("cls")
print("Loading ...")

import numpy as np
import pandas as pd


import difflib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Data Collection and PreProcessing

# loading the file
movies_data = pd.read_csv("movies.csv")

# selecting the relavent features for recommendation
selected_features = ["genres", "keywords", "tagline", "cast", "director"]

# replacing the null/missing values with null string

for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna('')
    
# combining all the 5 selected features
combined_features = movies_data['genres'] + ' ' + movies_data['keywords'] + ' ' + movies_data['tagline'] + ' ' + movies_data['cast'] + ' ' + movies_data['director'] 

# combining the text data to features vector
vectorizer = TfidfVectorizer()

feature_vector = vectorizer.fit_transform(combined_features)

# Cosine Similarity
# getting the similarity using cosine similarity

similarity = cosine_similarity(feature_vector)

# getting the movie name from the user

# creating the list of all the movies in the dataset
list_of_all_titles = movies_data['title'].tolist()
list_of_all_directors = movies_data['director'].tolist()
list_of_all_release_dates = movies_data['release_date'].tolist()
list_of_all_ratings = movies_data['vote_average'].tolist()

def DisplayMovie(movie):
    list_of_movies_name = []
    list_of_movies_director = []
    list_of_movies_release_dates = []
    list_of_movies_ratings = []

    # movie_name = input("Enter your favourite movie name")
    movie_name = movie

    #finding the close match for the movie name given by the user
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

    if len(find_close_match) == 0:
        return [],[],[],[]


    close_match = find_close_match[0]

    #finding the index of the movie with title
    index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

    #getting the list of similar movies
    similarity_score = list(enumerate(similarity[index_of_the_movie]))

    #sorting the movies based on their similarity score
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)
    
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = movies_data[movies_data.index == index]['index'].values[0]
        if i <= 50:
            list_of_movies_name.append(list_of_all_titles[title_from_index])
            list_of_movies_director.append(list_of_all_directors[title_from_index])
            list_of_movies_release_dates.append(list_of_all_release_dates[title_from_index])
            list_of_movies_ratings.append(list_of_all_ratings[title_from_index])
    
    return list_of_movies_name, list_of_movies_director, list_of_movies_release_dates, list_of_movies_ratings

def Display(name, director, release_date, rating):
    
    print("-----------------------------------------------------")
    print("Movie Name :", name)
    print("Directed by :", director)
    print("Release Date :", release_date)
    ratingText = str(rating) + "/10"
    print("Ratings : ", ratingText)

while True:

    os.system("cls")

    name = input("Enter a movie name: ")

    os.system("cls")
    print("Searching...")    
    movies_list, movies_director, movies_dates, movies_rating = DisplayMovie(name)

    os.system("cls")
    
    if len(movies_list) > 0:
        print("Movies suggested for you:  \n")
        for x in range(0,10):
            Display(movies_list[x], movies_director[x], movies_dates[x], movies_rating[x])
        
    else:
        print("No Movies Found")

    input("Press any key to continue...")