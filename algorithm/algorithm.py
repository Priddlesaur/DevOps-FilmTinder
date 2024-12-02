from collections import Counter
from datetime import datetime

ratings_data = [
    {'user_id': 1, 'movie_id': 10, 'rating': 5},
    {'user_id': 1, 'movie_id': 20, 'rating': 3},
    {'user_id': 2, 'movie_id': 10, 'rating': 4},
    {'user_id': 2, 'movie_id': 30, 'rating': 5},
    {'user_id': 3, 'movie_id': 10, 'rating': 2},
    {'user_id': 3, 'movie_id': 20, 'rating': 3},
    {'user_id': 3, 'movie_id': 30, 'rating': 4},
    {'user_id': 4, 'movie_id': 20, 'rating': 5},
    {'user_id': 4, 'movie_id': 40, 'rating': 4},
    {'user_id': 5, 'movie_id': 10, 'rating': 4},
    {'user_id': 5, 'movie_id': 30, 'rating': 3},
    {'user_id': 6, 'movie_id': 20, 'rating': 2},
    {'user_id': 6, 'movie_id': 40, 'rating': 5},
    {'user_id': 7, 'movie_id': 50, 'rating': 3},
    {'user_id': 7, 'movie_id': 60, 'rating': 4},
    {'user_id': 8, 'movie_id': 10, 'rating': 5},
    {'user_id': 8, 'movie_id': 50, 'rating': 4},
    {'user_id': 9, 'movie_id': 30, 'rating': 2},
    {'user_id': 9, 'movie_id': 60, 'rating': 3},
    {'user_id': 1, 'movie_id': 70, 'rating': 4},
    {'user_id': 1, 'movie_id': 80, 'rating': 3},
    {'user_id': 2, 'movie_id': 70, 'rating': 5},
    {'user_id': 2, 'movie_id': 80, 'rating': 4},
    {'user_id': 3, 'movie_id': 70, 'rating': 3},
    {'user_id': 4, 'movie_id': 80, 'rating': 5},
    {'user_id': 5, 'movie_id': 70, 'rating': 4},
    {'user_id': 6, 'movie_id': 70, 'rating': 2},
    {'user_id': 7, 'movie_id': 80, 'rating': 4},
    {'user_id': 8, 'movie_id': 80, 'rating': 3},
]

movies_data = {
    10: {'runtime': 120, 'release_date': '2001-07-20', 'title': 'Action Adventure', 'genre': 'Action'},
    20: {'runtime': 95, 'release_date': '2019-05-10', 'title': 'Romantic Comedy', 'genre': 'Romance'},
    30: {'runtime': 130, 'release_date': '2005-11-22', 'title': 'Sci-Fi Epic', 'genre': 'Sci-Fi'},
    40: {'runtime': 100, 'release_date': '2011-03-15', 'title': 'Crime Thriller', 'genre': 'Crime'},
    50: {'runtime': 110, 'release_date': '2016-08-01', 'title': 'Fantasy Drama', 'genre': 'Fantasy'},
    60: {'runtime': 140, 'release_date': '2020-02-25', 'title': 'Historical Drama', 'genre': 'Drama'},
    70: {'runtime': 125, 'release_date': '2015-11-15', 'title': 'Superhero Action', 'genre': 'Action'},
    80: {'runtime': 105, 'release_date': '2018-06-12', 'title': 'Action Thriller', 'genre': 'Action'},
    90: {'runtime': 98, 'release_date': '2021-01-30', 'title': 'Romantic Drama', 'genre': 'Romance'},
    100: {'runtime': 142, 'release_date': '2017-08-22', 'title': 'Sci-Fi Adventure', 'genre': 'Sci-Fi'},
    110: {'runtime': 105, 'release_date': '2019-09-10', 'title': 'Mystery Thriller', 'genre': 'Crime'},
    120: {'runtime': 98, 'release_date': '2016-12-05', 'title': 'Fantasy Quest', 'genre': 'Fantasy'},
    130: {'runtime': 130, 'release_date': '2023-05-19', 'title': 'Historical Epic', 'genre': 'Drama'},
}

# Stap 1: User-Item Matrix
user_item_matrix = {}
for entry in ratings_data:
    user_id = entry['user_id']
    movie_id = entry['movie_id']
    rating = entry['rating']

    if user_id not in user_item_matrix:
        user_item_matrix[user_id] = {}
    user_item_matrix[user_id][movie_id] = rating

# Haal alle unieke film ID's op uit de beoordelingen
all_movies = {entry['movie_id'] for entry in ratings_data}

# Itereer door de beoordelingen van iedere gebruiker
for user_ratings in user_item_matrix.values():
    for movie in all_movies:
        if movie not in user_ratings:
            user_ratings[movie] = None


def cosine_similarity(user1, user2):
    common_movies = [
        movie for movie in user_item_matrix[user1]
        if
        movie in user_item_matrix[user2] and user_item_matrix[user1][movie] > 0 and user_item_matrix[user2][movie] > 0
    ]
    if not common_movies:
        return 0  # Geen gedeelde beoordelingen, gelijkenis is 0

    ratings1 = [user_item_matrix[user1][movie] for movie in common_movies]
    ratings2 = [user_item_matrix[user2][movie] for movie in common_movies]

    dot_product = sum(r1 * r2 for r1, r2 in zip(ratings1, ratings2))
    norm1 = sum(r ** 2 for r in ratings1) ** 0.5
    norm2 = sum(r ** 2 for r in ratings2) ** 0.5

    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0

# Cosinusgelijkenis
# def cosine_similarity(user1, user2):
#     ratings1 = list(user_item_matrix[user1].values())
#     ratings2 = list(user_item_matrix[user2].values())
#     dot_product = sum(r1 * r2 for r1, r2 in zip(ratings1, ratings2))
#     norm1 = sum(r ** 2 for r in ratings1) ** 0.5
#     norm2 = sum(r ** 2 for r in ratings2) ** 0.5
#     return dot_product / (norm1 * norm2) if norm1 and norm2 else 0


def get_top_k_similar_users(user_id, k=2):
    similarities = {}
    for other_user in user_item_matrix:
        if other_user != user_id:
            similarity = cosine_similarity(user_id, other_user)
            similarities[other_user] = similarity
    top_k_users = sorted(similarities, key=similarities.get, reverse=True)[:k]
    return top_k_users


# Functie voor het berekenen van een 'tijd en release' gewicht
def time_release_weight(movie_id, preferred_runtime, preferred_release_year):
    runtime = movies_data[movie_id]['runtime']
    runtime_weight = max(0, 1 - abs(runtime - preferred_runtime) / 100)

    release_year = datetime.strptime(movies_data[movie_id]['release_date'], "%Y-%m-%d").year
    release_weight = max(0, 1 - abs(release_year - preferred_release_year) / 20)

    return (runtime_weight + release_weight) / 2


# Functie om automatisch de voorkeuren van de gebruiker te bepalen
def get_user_preferences(user_id):
    liked_movies = [movie_id for movie_id, rating in user_item_matrix[user_id].items() if rating > 3]
    if not liked_movies:
        return 100, 2010  # Standaard waarden als geen films zijn geliket

    total_runtime = sum(movies_data[movie_id]['runtime'] for movie_id in liked_movies)
    total_year = sum(
        datetime.strptime(movies_data[movie_id]['release_date'], "%Y-%m-%d").year for movie_id in liked_movies)

    preferred_runtime = total_runtime / len(liked_movies)
    preferred_release_year = total_year / len(liked_movies)

    return preferred_runtime, preferred_release_year


# Functie om het favoriete genre van een gebruiker te bepalen
def get_user_favorite_genre(user_id):
    liked_movies = [movie_id for movie_id, rating in user_item_matrix[user_id].items() if rating > 3]
    if not liked_movies:
        return None  # Geen favoriete genre als er geen films geliket zijn

    liked_genres = [movies_data[movie_id]['genre'] for movie_id in liked_movies]
    genre_counts = Counter(liked_genres)
    favorite_genre = genre_counts.most_common(1)[0][0]
    return favorite_genre


# Functie om een genregewicht toe te voegen
def genre_weight(movie_id, favorite_genre):
    return 1.2 if movies_data[movie_id]['genre'] == favorite_genre else 1.0


# Aangepaste predictie functie om tijd, release en genre mee te nemen
def predict_rating(user_id, movie_id, k=2):
    preferred_runtime, preferred_release_year = get_user_preferences(user_id)
    favorite_genre = get_user_favorite_genre(user_id)

    top_k_users = get_top_k_similar_users(user_id, k)
    ratings = []
    similarities = []

    for other_user in top_k_users:
        rating = user_item_matrix[other_user][movie_id]
        if rating > 0:
            ratings.append(rating)
            similarities.append(cosine_similarity(user_id, other_user))

    if not ratings:
        return None

    weighted_ratings = sum(r * s for r, s in zip(ratings, similarities)) / sum(similarities)

    # Voeg tijd, release en genre gewicht toe aan de voorspelling
    tr_weight = time_release_weight(movie_id, preferred_runtime, preferred_release_year)
    genre_factor = genre_weight(movie_id, favorite_genre)

    final_rating = weighted_ratings * tr_weight * genre_factor
    return final_rating


# Aanbevelingen genereren met tijd, release en genre voorkeuren
def recommend_movies(user_id, k=2, top_n=3):
    user_ratings = user_item_matrix[user_id]
    unrated_movies = [movie for movie, rating in user_ratings.items() if rating == 0]

    predictions = []
    for movie_id in unrated_movies:
        predicted_rating = predict_rating(user_id, movie_id, k)
        if predicted_rating is not None:
            predictions.append((movie_id, predicted_rating))

    predictions.sort(key=lambda x: x[1], reverse=True)
    recommended_movies = [movie for movie, rating in predictions[:top_n]]

    # Haal de titels van de aanbevolen films op
    recommended_movie_titles = [movies_data[movie_id]['title'] for movie_id in recommended_movies]

    return recommended_movie_titles


# Voorbeeld van gebruik
user_id = 2
recommended_movie_titles = recommend_movies(user_id)
print(f"Aanbevelingen voor gebruiker {user_id}: {recommended_movie_titles}")
