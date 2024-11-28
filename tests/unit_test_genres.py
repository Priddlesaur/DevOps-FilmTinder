import pytest
from fastapi.testclient import TestClient

from dtos.dtos import GenreDto
from main import app
from unittest.mock import MagicMock
from models.base import User, Genre
from routers.genres import read_genres, read_genre

Test = TestClient(app)

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_read_genres():
    mock_db = MagicMock()
    mock_genre_1 = MagicMock(spec=Genre)
    mock_genre_2 = MagicMock(spec=Genre)

    mock_genre_1.id = 1
    mock_genre_2.id = 2

    mock_genre_1.name = 'Genre 1'
    mock_genre_2.name = 'Genre 2'

    mock_db.query.return_value.all.return_value = [mock_genre_1, mock_genre_2]

    result = await read_genres(db=mock_db)

    assert result[0].id == mock_genre_1.id
    assert result[0].name == mock_genre_1.name
    assert result[1].id == mock_genre_2.id
    assert result[1].name == mock_genre_2.name

@pytest.mark.asyncio
async def test_read_genre():
    mock_db = MagicMock()
    mock_genre = MagicMock(spec=Genre)
    mock_genre.id = 1
    mock_genre.name = 'Genre 1'
    mock_db.query.return_value.get.return_value = mock_genre

    result = await read_genre(genre_id = mock_genre.id, db=mock_db)

    assert result.id == mock_genre.id
    assert result.name == mock_genre.name

@pytest.mark.asyncio
async def test_create_movie():
    mock_db = MagicMock()
    mock_movie = GenreDto(id=1, title='Titanic', release_date=datetime(2001,11,11), runtime=120, imdb_id=1, genre_id=1)

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = await create_movie(movie=mock_movie, db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.id == mock_movie.id
    assert result.title == mock_movie.title
    assert result.release_date == mock_movie.release_date
    assert result.runtime == mock_movie.runtime
    assert result.imdb_id == mock_movie.imdb_id
    assert result.genre_id == mock_movie.genre_id





