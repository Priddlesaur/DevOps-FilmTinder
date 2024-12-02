import pytest
from fastapi.testclient import TestClient

from dtos.dtos import GenreDto, GenreBaseDto
from main import app
from unittest.mock import MagicMock
from models.base import Genre
from routers.genres import read_genres, read_genre, create_genre, update_genre, delete_genre

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
async def test_create_genre():
    mock_db = MagicMock()
    mock_response = MagicMock()
    mock_genre = GenreDto(id=1, name='Horror')

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = await create_genre(genre=mock_genre, response= mock_response,db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.id == mock_genre.id
    assert result.name == mock_genre.name
    mock_response.status_code = 201
    mock_response.headers["Location"] = f"/genres/{result.id}"

@pytest.mark.asyncio
async def test_upgrade_genre():
    mock_db = MagicMock()

    genre_id = 1
    existing_genre = GenreDto(id=genre_id, name='Horror')
    updated_genre = GenreBaseDto(name='Horror/Mysterie')

    mock_db.query.return_value.filter_by.return_value.first.return_value = existing_genre

    result = await update_genre(genre_id = genre_id, updated_genre = updated_genre, db=mock_db)

    mock_db.query.return_value.filter_by.assert_called_once_with(id=genre_id)
    mock_db.commit.assert_called_once()

    assert existing_genre.name == updated_genre.name
    assert result.name == updated_genre.name
    assert result.id == genre_id

@pytest.mark.asyncio
async def test_delete_genre():
    mock_db = MagicMock()
    genre_id = 1
    mock_genre = GenreDto(id=genre_id, name='Horror')

    mock_db.query.return_value.filter.return_value.first.return_value = mock_genre

    result = await delete_genre(genre_id = mock_genre.id, db=mock_db)

    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

    assert result == {"message": f"Genre with {genre_id} has been deleted"}






