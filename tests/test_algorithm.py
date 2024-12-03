# test_recommendation_algorithm.py
import pytest
import pandas as pd
from algorithm.algorithm import (
    build_user_item_matrix, cosine_similarity_matrix, recommend_movies
)

# Mock data
ratings_data = pd.DataFrame({
    'user_id': [1, 1, 2, 2, 3, 3],
    'movie_id': [1, 2, 1, 3, 2, 3],
    'rating': [5, 4, 4, 5, 3, 2]
})

movies_data = pd.DataFrame({
    'movie_id': [1, 2, 3],
    'title': ['Movie 1', 'Movie 2', 'Movie 3'],
    'genre': ['Action', 'Comedy', 'Drama'],
    'runtime': [120, 90, 150],
    'release_date': ['2000-01-01', '2005-01-01', '2010-07-15']
})

def test_build_user_item_matrix():
    user_item_matrix = build_user_item_matrix(ratings_data)
    assert user_item_matrix.shape == (3, 3)
    assert user_item_matrix.loc[1, 1] == 5
    assert user_item_matrix.loc[2, 3] == 5

def test_cosine_similarity_matrix():
    user_item_matrix = build_user_item_matrix(ratings_data)
    similarity_matrix = cosine_similarity_matrix(user_item_matrix)
    assert similarity_matrix.shape == (3, 3)
    assert similarity_matrix[0, 1] > 0  # Check if similarity is calculated


def test_recommend_movies():
    user_item_matrix = build_user_item_matrix(ratings_data)
    similarity_matrix = cosine_similarity_matrix(user_item_matrix)
    recommendations = recommend_movies(1, user_item_matrix, similarity_matrix, movies_data, k=2, top_n=2)

    print(f"Recommendations: {recommendations}")

    assert len(recommendations) == 1
    assert recommendations[0] in ['Movie 3']

@pytest.mark.asyncio
async def test_get_user_recommendations():
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)
    response = client.get("/users/1/recommend")
    assert response.status_code == 200
    assert len(response.json()) > 0