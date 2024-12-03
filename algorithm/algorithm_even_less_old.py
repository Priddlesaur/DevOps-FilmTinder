import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from models.base import Rating, Movie
from database import get_db


def load_data_from_db():
    """
    Laadt ratings en movies vanuit de database en converteert naar Pandas DataFrames.
    """
    db: Session = next(get_db())

    # Ratings ophalen
    ratings_query = db.query(Rating).all()
    ratings_data = pd.DataFrame([
        {'user_id': rating.user_id, 'movie_id': rating.movie_id, 'rating': rating.rating}
        for rating in ratings_query
    ])

    # Movies ophalen
    movies_query = db.query(Movie).all()
    movies_data = pd.DataFrame([
        {
            'movie_id': movie.id,
            'runtime': movie.runtime,
            'release_date': movie.release_date.strftime('%Y-%m-%d'),
            'title': movie.title,
            'genre': movie.genre
        }
        for movie in movies_query
    ])

    return ratings_data, movies_data


def build_user_item_matrix(ratings_data):
    """
    Bouwt de User-Item matrix als een Pandas DataFrame.
    """
    user_item_matrix = ratings_data.pivot(index='user_id', columns='movie_id', values='rating')
    return user_item_matrix


# --- Similarity functies ---
def cosine_similarity_matrix(user_item_matrix):
    """
    Bereken de Cosine Similarity matrix tussen alle gebruikers.
    """
    matrix = user_item_matrix.fillna(0).values
    norms = np.linalg.norm(matrix, axis=1)
    similarity_matrix = np.dot(matrix, matrix.T) / (norms[:, None] * norms[None, :])
    np.fill_diagonal(similarity_matrix, 0)  # Gelijkenis met zichzelf is 0
    return similarity_matrix


# --- Gebruikersvoorkeuren ophalen ---
def get_user_preferences(user_id, user_item_matrix, movies_data):
    """
    Haalt voorkeuren van een gebruiker op: runtime, release jaar en favoriete genre.
    """
    user_ratings = user_item_matrix.loc[user_id]
    liked_movies = user_ratings[user_ratings > 3].index

    if liked_movies.empty:
        return 100, 2010, None

    preferred_runtime = movies_data.loc[movies_data['movie_id'].isin(liked_movies), 'runtime'].mean()
    preferred_release_year = movies_data.loc[movies_data['movie_id'].isin(liked_movies), 'release_date'].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d").year).mean()
    favorite_genre = movies_data.loc[movies_data['movie_id'].isin(liked_movies), 'genre'].mode().iloc[0]

    return preferred_runtime, preferred_release_year, favorite_genre

def time_release_weight(movie_id, preferred_runtime, preferred_release_year, movies_data):
    """
    Berekent de tijd- en releasegewichten voor een film.
    """
    movie = movies_data[movies_data['movie_id'] == movie_id].iloc[0]
    runtime_weight = max(0, 1 - abs(movie['runtime'] - preferred_runtime) / 100)
    release_year = datetime.strptime(movie['release_date'], "%Y-%m-%d").year
    release_weight = max(0, 1 - abs(release_year - preferred_release_year) / 20)
    return (runtime_weight + release_weight) / 2


def genre_weight(movie_id, favorite_genre, movies_data):
    """
    Berekent het genrewicht voor een film.
    """
    genre = movies_data.loc[movies_data['movie_id'] == movie_id, 'genre'].iloc[0]
    return 1.2 if genre == favorite_genre else 1.0


# --- Beoordelingen voorspellen ---
def predict_rating(user_id, movie_id, similarity_matrix, user_item_matrix, movies_data, k=2):
    """
    Voorspelt de beoordeling van een gebruiker voor een film.
    """
    user_index = user_item_matrix.index.get_loc(user_id)
    top_k_users = np.argsort(similarity_matrix[user_index])[-k:]

    ratings = []
    similarities = []
    for similar_user in top_k_users:
        similar_user_id = user_item_matrix.index[similar_user]
        rating = user_item_matrix.loc[similar_user_id, movie_id]

        if not np.isnan(rating):
            ratings.append(rating)
            similarities.append(similarity_matrix[user_index, similar_user])

    if not ratings or sum(similarities) == 0:
        return None

    weighted_ratings = sum(r * s for r, s in zip(ratings, similarities)) / sum(similarities)

    preferred_runtime, preferred_release_year, favorite_genre = get_user_preferences(user_id, user_item_matrix, movies_data)
    tr_weight = time_release_weight(movie_id, preferred_runtime, preferred_release_year, movies_data)
    genre_factor = genre_weight(movie_id, favorite_genre, movies_data)

    return weighted_ratings * tr_weight * genre_factor

# --- Aanbevelingen maken ---
def recommend_movies(user_id, user_item_matrix, similarity_matrix, movies_data, k=2, top_n=3):
    """
    Geeft een lijst met aanbevolen films voor een gebruiker.
    """
    user_ratings = user_item_matrix.loc[user_id]
    unrated_movies = user_ratings[user_ratings.isna()].index

    predictions = []
    for movie_id in unrated_movies:
        predicted_rating = predict_rating(user_id, movie_id, similarity_matrix, user_item_matrix, movies_data, k)
        if predicted_rating is not None:
            predictions.append((movie_id, predicted_rating))

    predictions.sort(key=lambda x: x[1], reverse=True)
    recommended_movies = [movies_data.loc[movies_data['movie_id'] == movie_id, 'title'].iloc[0] for movie_id, _ in predictions[:top_n]]

    return recommended_movies
