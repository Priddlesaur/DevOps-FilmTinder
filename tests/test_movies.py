from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from dtos.dtos import MovieDto
from main import app
from unittest.mock import MagicMock
from models.base import Movie
from routers.movies import read_movies, read_movie, create_movie, update_movie, delete_movie

Test = TestClient(app)

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_read_movies():
    mock_db = MagicMock()
    mock_movie_1 = MagicMock(spec=Movie, id=1, title='LOTR', release_date=datetime(2001,11,11), runtime=100, imdb_id='123', genre_id=1)
    mock_movie_2 = MagicMock(spec=Movie, id=2, title='LOTR2', release_date=datetime(2001,1,1), runtime=120, imdb_id='123', genre_id=2)

    mock_db.query.return_value.all.return_value = [mock_movie_1, mock_movie_2]

    result = await read_movies(db=mock_db)

    assert result[0].id == mock_movie_1.id
    assert result[0].title == mock_movie_1.title
    assert result[0].release_date == mock_movie_1.release_date
    assert result[0].runtime == mock_movie_1.runtime
    assert result[0].imdb_id == mock_movie_1.imdb_id
    assert result[0].genre_id == mock_movie_1.genre_id

    assert result[1].id == mock_movie_2.id
    assert result[1].title == mock_movie_2.title
    assert result[1].release_date == mock_movie_2.release_date
    assert result[1].runtime == mock_movie_2.runtime
    assert result[1].imdb_id == mock_movie_2.imdb_id
    assert result[1].genre_id == mock_movie_2.genre_id

@pytest.mark.asyncio
async def test_read_movie():
    mock_db = MagicMock()
    mock_movie = MagicMock(spec=Movie, id=1, title='LOTR', release_date=datetime(2001,11,11), runtime=100, imdb_id='123', genre_id=1)

    mock_db.query.return_value.get.return_value = mock_movie

    result = await read_movie(movie_id=mock_movie.id, db=mock_db)

    assert result.id == mock_movie.id
    assert result.title == mock_movie.title
    assert result.release_date == mock_movie.release_date
    assert result.runtime == mock_movie.runtime
    assert result.imdb_id == mock_movie.imdb_id
    assert result.genre_id == mock_movie.genre_id

@pytest.mark.asyncio
async def test_create_movie():
    mock_db = MagicMock()
    mock_response = MagicMock()
    mock_movie = MovieDto(id=1, title='Titanic', release_date=datetime(2001,11,11), runtime=120, imdb_id='123', genre_id=1)

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = await create_movie(movie=mock_movie, response=mock_response, db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.id == mock_movie.id
    assert result.title == mock_movie.title
    assert result.release_date == mock_movie.release_date
    assert result.runtime == mock_movie.runtime
    assert result.imdb_id == mock_movie.imdb_id
    assert result.genre_id == mock_movie.genre_id

#bijwerken
@pytest.mark.asyncio
async def test_update_movie():
    mock_db = MagicMock()
    movie_id = 1
    existing_movie = Movie(id = movie_id, title = 'Titanic',
    release_date = datetime(2001,11,11), runtime=120, imdb_id='123', genre_id=1)
    updated_movie = MovieDto(title = 'Titanic2', release_date = datetime(2001,11,11), runtime=120, imdb_id='123', genre_id=1)

    mock_db.query.return_value.filter_by.return_value.first.return_value = existing_movie

    result = await update_movie(movie_id = movie_id, updated_movie = updated_movie, db=mock_db)

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.title == updated_movie.title
    assert result.release_date == updated_movie.release_date
    assert result.runtime == updated_movie.runtime
    assert result.imdb_id == updated_movie.imdb_id
    assert result.genre_id == updated_movie.genre_id

@pytest.mark.asyncio
async def test_delete_movie():
    mock_db = MagicMock()
    movie_id = 1
    mock_movie = Movie(id = movie_id, title = 'Titanic', release_date=datetime(2001,11,11), runtime=120, imdb_id='123', genre_id=1)

    mock_db.query.return_value.filter.return_value.first.return_value = mock_movie

    result = await delete_movie(movie_id = movie_id, db=mock_db)

    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

    assert result == {"detail": f"Movie with ID {movie_id} has been deleted"}









