import pytest
from fastapi.testclient import TestClient

from dtos.dtos import UserDto
from main import app
from unittest.mock import MagicMock
from models.base import User
from routers.users import read_user, get_users, create_user, update_user, delete_user

Test = TestClient(app)

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_get_users():
    # Arrange
    mock_db = MagicMock()
    mock_users = [
        MagicMock(spec=User, id=1, username='us1', first_name='fn1', last_name='ln1'),
        MagicMock(spec=User, id=2, username='us2', first_name='fn2', last_name='ln2'),
        MagicMock(spec=User, id=3, username='us3', first_name='fn3', last_name='ln3')
    ]
    mock_db.query.return_value.all.return_value = mock_users

    # Act
    result = await get_users(db=mock_db)

    # Assert
    assert all(user.id in [1,2,3] for user in result)
    assert all(user.username in ['us1', 'us2', 'us3'] for user in result)
    assert all(user.first_name in ['fn1', 'fn2', 'fn3'] for user in result)
    assert all(user.last_name in ['ln1', 'ln2', 'ln3'] for user in result)

@pytest.mark.asyncio
async def test_read_user():
    #Arrange
    mock_db = MagicMock()
    mock_user = MagicMock(spec=User)
    mock_user.id = 1
    mock_user.username = 'us1'
    mock_user.first_name = 'fn1'
    mock_user.last_name = 'ln1'
    mock_db.query.return_value.get.return_value = mock_user

    #Act
    result = await read_user(user_id = mock_user.id, db=mock_db)

    #Assert
    assert result.id == mock_user.id
    assert result.username == 'us1'
    assert result.first_name == 'fn1'
    assert result.last_name == 'ln1'

@pytest.mark.asyncio
async def test_create_user():
    mock_db = MagicMock()
    mock_user = UserDto(username = 'us1', first_name = 'fn1', last_name = 'ln1')

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = await create_user(user=mock_user, db=mock_db)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert "User added successfully" in result
    assert result["User added successfully"].username == "us1"
    assert result["User added successfully"].first_name == "fn1"
    assert result["User added successfully"].last_name == "ln1"

# @pytest.mark.asyncio
# async def test_update_user():
#     mock_db = MagicMock()
#     user_id = 1
#     existing_user = User(id = user_id, username='oldname', first_name='old', last_name='old')
#     updated_user = UserDto(username='newname', first_name='new', last_name='new')
#
#     mock_db.query.return_value.filter_by.return_value.first.return_value = existing_user
#
#     result = await update_user(user_id = user_id, user = updated_user, db=mock_db)
#
#     mock_db.commit.assert_called_once()
#     mock_db.refresh.assert_called_once()
#
#     assert result == {"User updated successfully": updated_user}

@pytest.mark.asyncio
async def test_delete_user():
    mock_db = MagicMock()
    mock_id = 1
    mock_user = User(id = mock_id, username = 'us1', first_name = 'fn1', last_name = 'ln1')

    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    result = await delete_user(user_id = mock_user.id, db=mock_db)

    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()

    assert result == {"message": f"User with {mock_id} has been deleted"}















