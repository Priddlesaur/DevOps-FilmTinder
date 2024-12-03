import pytest
from fastapi.testclient import TestClient

from dtos.dtos import UserDto
from main import app
from unittest.mock import MagicMock
from models.base import User
from routers.users import read_user, read_users, create_user, update_user, delete_user

Test = TestClient(app)

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_get_users():
    # Arrange
    mock_db = MagicMock()
    mock_users = [
        MagicMock(spec=User, id=1, username='user1', first_name='firstname1', last_name='lastname1'),
        MagicMock(spec=User, id=2, username='user2', first_name='firstname2', last_name='lastname2'),
        MagicMock(spec=User, id=3, username='user3', first_name='firstname3', last_name='lastname3')
    ]
    mock_db.query.return_value.all.return_value = mock_users

    # Act
    result = await read_users(db=mock_db)

    # Assert
    assert all(user.id in [1,2,3] for user in result)
    assert all(user.username in ['user1', 'user2', 'user3'] for user in result)
    assert all(user.first_name in ['firstname1', 'firstname2', 'firstname3'] for user in result)
    assert all(user.last_name in ['lastname1', 'lastname2', 'lastname3'] for user in result)

@pytest.mark.asyncio
async def test_read_user():
    #Arrange
    mock_db = MagicMock()
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = 'user1'
    mock_user.first_name = 'firstname1'
    mock_user.last_name = 'lastname1'
    mock_db.query.return_value.get.return_value = mock_user

    #Act
    result = await read_user(user_id = mock_user.id, db=mock_db)

    #Assert
    assert result.id == mock_user.id
    assert result.username == 'user1'
    assert result.first_name == 'firstname1'
    assert result.last_name == 'lastname1'

@pytest.mark.asyncio
async def test_create_user():
    mock_db = MagicMock()
    mock_response = MagicMock()
    mock_user = UserDto(username = 'user1', first_name = 'firstname1', last_name = 'lastname1')

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = await create_user(user=mock_user, response = mock_response, db =mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.username == mock_user.username
    assert result.first_name == mock_user.first_name
    assert result.last_name == mock_user.last_name

@pytest.mark.asyncio
async def test_update_user():
    mock_db = MagicMock()
    user_id = 1
    existing_user = User(id = user_id, username='username', first_name='oldfirst', last_name='oldlast')
    updated_user = UserDto(username='newname', first_name='newfirst', last_name='newfirst')

    mock_db.query.return_value.filter_by.return_value.first.return_value = existing_user

    result = await update_user(user_id = user_id, updated_user= updated_user, db=mock_db)

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.username == updated_user.username
    assert result.first_name == updated_user.first_name
    assert result.last_name == updated_user.last_name

@pytest.mark.asyncio
async def test_delete_user():
    mock_db = MagicMock()
    mock_id = 1
    mock_user = User(id = mock_id, username = 'user1', first_name = 'firstname1', last_name = 'lastname1')

    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    result = await delete_user(user_id=mock_user.id, db=mock_db)

    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

    assert result == {"message": f"User with {mock_id} has been deleted"}











