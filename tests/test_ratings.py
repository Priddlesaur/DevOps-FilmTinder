from datetime import datetime
from os import lchmod

import pytest
from fastapi.testclient import TestClient

from dtos.dtos import GenreDto, GenreBaseDto, RatingBaseDto, RatingDto
from main import app
from unittest.mock import MagicMock
from models.base import Rating
from routers.ratings import get_ratings, get_rating, create_rating, delete_rating, update_rating

Test = TestClient(app)

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_get_ratings():
    mock_db = MagicMock()
    mock_ratings = [
        MagicMock(spec=Rating, id = 1, movie_id = 1, user_id = 1, rating = 3, date = datetime(2020, 1, 1)),
        MagicMock(spec=Rating, id = 2, movie_id = 2, user_id = 2, rating = 4, date = datetime(2020, 1, 5)),
    ]

    mock_db.query.return_value.all.return_value = mock_ratings

    result = await get_ratings(mock_db)

    assert result[0].movie_id == mock_ratings[0].movie_id
    assert result[0].user_id == mock_ratings[0].user_id
    assert result[0].rating == mock_ratings[0].rating
    assert result[0].date == mock_ratings[0].date
    assert result[1].movie_id == mock_ratings[1].movie_id
    assert result[1].user_id == mock_ratings[1].user_id
    assert result[1].rating == mock_ratings[1].rating
    assert result[1].date == mock_ratings[1].date

@pytest.mark.asyncio
async def test_get_rating():
    mock_db = MagicMock()
    rating_id = 1
    mock_rating = MagicMock(spec=Rating, id = 1, movie_id = 1, user_id = 1, rating = 3, date = datetime(2020, 1, 1))

    mock_db.query.return_value.get.return_value = mock_rating

    result = await get_rating(rating_id = rating_id, db = mock_db)

    assert result.movie_id == mock_rating.movie_id
    assert result.user_id == mock_rating.user_id
    assert result.rating == mock_rating.rating
    assert result.date == mock_rating.date

@pytest.mark.asyncio
async def test_create_rating():
    mock_db = MagicMock()
    mock_response = MagicMock()
    mock_rating = RatingDto(id = 1, movie_id = 1, user_id = 1, rating = 3, date = datetime(2020, 1, 1))

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = await create_rating(rating = mock_rating, response = mock_response, db = mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.movie_id == mock_rating.movie_id
    assert result.user_id == mock_rating.user_id
    assert result.rating == mock_rating.rating
    assert result.date == mock_rating.date
    mock_response.status_code = 201
    mock_response.headers["Location"] = f"/ratings/{result.id}"

@pytest.mark.asyncio
async def test_update_rating():
    mock_db = MagicMock()
    rating_id = 1
    existing_rating = Rating(id = rating_id, movie_id = 1, user_id = 1, rating = 3, date = datetime(2020, 1, 1))
    updated_rating = RatingDto(movie_id = 1, user_id = 1, rating = 5, date = datetime(2020, 1, 1))

    mock_db.query.return_value.filter_by.return_value.first.return_value = existing_rating

    result = await update_rating(rating_id = rating_id, updated_rating = updated_rating, db = mock_db)

    mock_db.commit.assert_called_once()

    assert existing_rating.user_id == updated_rating.user_id
    assert existing_rating.rating == updated_rating.rating
    assert existing_rating.date == updated_rating.date
    assert result.movie_id == updated_rating.movie_id
    assert result.user_id == updated_rating.user_id
    assert result.rating == updated_rating.rating
    assert result.date == updated_rating.date

@pytest.mark.asyncio
async def test_delete_rating():
    mock_db = MagicMock()
    rating_id = 1
    mock_rating = RatingDto(id = rating_id, movie_id = 1, user_id = 1, rating = 3, date = datetime(2020, 1, 1))

    mock_db.query.return_value.filter.return_value.first.return_value = mock_rating

    result = await delete_rating(rating_id = rating_id, db = mock_db)

    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

    assert result == {"message": f"Rating with {rating_id} has been deleted"}

