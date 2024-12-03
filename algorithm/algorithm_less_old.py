from collections import Counter
from datetime import datetime
from sqlalchemy.orm import Session
from models.base import Rating, Movie
from database import get_db


def load_data_from_db():
    """
    Laadt ratings en movies vanuit de database.
    """
    db: Session = next(get_db())

    # Ratings ophalen
    ratings_query = db.query(Rating).all()
    ratings_data = [
        {'user_id': rating.user_id, 'movie_id': rating.movie_id, 'rating': rating.rating}
        for rating in ratings_query
    ]

    # Movies ophalen
    movies_query = db.query(Movie).all()
    movies_data = {
        movie.id: {
            'runtime': movie.runtime,
            'release_date': movie.release_date.strftime('%Y-%m-%d'),
            'title': movie.title,
            'genre': movie.genre
        }
        for movie in movies_query
    }

    return ratings_data, movies_data


def build_user_item_matrix(ratings_data):
    """
    Bouwt de User-Item matrix op uit de ratings.
    """
    user_item_matrix = {}
    for entry in ratings_data:
        user_id = entry['user_id']
        movie_id = entry['movie_id']
        rating = entry['rating']

        if user_id not in user_item_matrix:
            user_item_matrix[user_id] = {}
        user_item_matrix[user_id][movie_id] = rating

    # Haal alle unieke film-ID's op
    all_movies = {entry['movie_id'] for entry in ratings_data}

    # Vul de matrix aan met None voor films die niet beoordeeld zijn
    for user_ratings in user_item_matrix.values():
        for movie in all_movies:
            if movie not in user_ratings:
                user_ratings[movie] = None

    return user_item_matrix


# Gebruik dynamisch geladen data
ratings_data, movies_data = load_data_from_db()
user_item_matrix = build_user_item_matrix(ratings_data)


def cosine_similarity(user1, user2):
    ratings1 = user_item_matrix[user1]
    ratings2 = user_item_matrix[user2]

    common_movies = [
        movie for movie in ratings1 if ratings1[movie] is not None and ratings2[movie] is not None
    ]
    if not common_movies:
        return 0

    r1 = [ratings1[movie] for movie in common_movies]
    r2 = [ratings2[movie] for movie in common_movies]

    dot_product = sum(x * y for x, y in zip(r1, r2))
    norm1 = sum(x ** 2 for x in r1) ** 0.5
    norm2 = sum(y ** 2 for y in r2) ** 0.5

    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0


def get_top_k_similar_users(user_id, k=2):
    similarities = {}
    for other_user in user_item_matrix:
        if other_user != user_id:
            similarity = cosine_similarity(user_id, other_user)
            similarities[other_user] = similarity
    top_k_users = sorted(similarities, key=similarities.get, reverse=True)[:k]
    return top_k_users


def time_release_weight(movie_id, preferred_runtime, preferred_release_year):
    runtime = movies_data[movie_id]['runtime']
    runtime_weight = max(0, 1 - abs(runtime - preferred_runtime) / 100)

    release_year = datetime.strptime(movies_data[movie_id]['release_date'], "%Y-%m-%d").year
    release_weight = max(0, 1 - abs(release_year - preferred_release_year) / 20)

    return (runtime_weight + release_weight) / 2


def get_user_preferences(user_id):
    liked_movies = [movie_id for movie_id, rating in user_item_matrix[user_id].items() if rating is not None and rating > 3]
    if not liked_movies:
        return 100, 2010

    total_runtime = sum(movies_data[movie_id]['runtime'] for movie_id in liked_movies)
    total_year = sum(
        datetime.strptime(movies_data[movie_id]['release_date'], "%Y-%m-%d").year for movie_id in liked_movies)

    preferred_runtime = total_runtime / len(liked_movies)
    preferred_release_year = total_year / len(liked_movies)

    return preferred_runtime, preferred_release_year


def get_user_favorite_genre(user_id):
    liked_movies = [movie_id for movie_id, rating in user_item_matrix[user_id].items() if rating is not None and rating > 3]
    if not liked_movies:
        return None

    liked_genres = [movies_data[movie_id]['genre'] for movie_id in liked_movies]
    genre_counts = Counter(liked_genres)
    favorite_genre = genre_counts.most_common(1)[0][0]
    return favorite_genre


def genre_weight(movie_id, favorite_genre):
    return 1.2 if movies_data[movie_id]['genre'] == favorite_genre else 1.0


def predict_rating(user_id, movie_id, k=2):
    preferred_runtime, preferred_release_year = get_user_preferences(user_id)
    favorite_genre = get_user_favorite_genre(user_id)

    top_k_users = get_top_k_similar_users(user_id, k)
    ratings = []
    similarities = []

    for other_user in top_k_users:
        rating = user_item_matrix[other_user].get(movie_id)
        if rating is not None:
            ratings.append(rating)
            similarities.append(cosine_similarity(user_id, other_user))

    if not ratings or sum(similarities) == 0:
        # Geen gelijkenissen of beoordelingen beschikbaar
        return None

    weighted_ratings = sum(r * s for r, s in zip(ratings, similarities)) / sum(similarities)

    tr_weight = time_release_weight(movie_id, preferred_runtime, preferred_release_year)
    genre_factor = genre_weight(movie_id, favorite_genre)

    final_rating = weighted_ratings * tr_weight * genre_factor
    return final_rating

def recommend_movies(user_id, k=2, top_n=3):
    user_ratings = user_item_matrix[user_id]
    unrated_movies = [movie for movie, rating in user_ratings.items() if rating is None]

    predictions = []
    for movie_id in unrated_movies:
        predicted_rating = predict_rating(user_id, movie_id, k)
        if predicted_rating is not None:
            predictions.append((movie_id, predicted_rating))

    predictions.sort(key=lambda x: x[1], reverse=True)
    recommended_movies = [movie for movie, rating in predictions[:top_n]]

    recommended_movie_titles = [movies_data[movie_id]['title'] for movie_id in recommended_movies]

    return recommended_movie_titles
