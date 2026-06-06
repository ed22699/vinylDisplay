import pytest
from unittest.mock import patch, MagicMock, mock_open
from vinyl_dashboard.utils.discogs_sync import discogs_sync

@patch('builtins.open', new_callable=mock_open, read_data='discogs:\n  token: fake_token\n  username: configuser')
@patch('yaml.safe_load')
@patch('vinyl_dashboard.utils.discogs_sync.discogs')
@patch('vinyl_dashboard.utils.discogs_sync.LocalLibrary')
def test_sync_library_with_username(mock_local_library, mock_discogs_class, mock_safe_load, mock_open_file):
    # Arrange
    mock_config = {'discogs': {'token': 'fake_token', 'username': 'configuser'}}
    mock_safe_load.return_value = mock_config
    
    mock_discogs_instance = MagicMock()
    mock_discogs_instance.get_user_collection.return_value = {'releases': []}
    mock_discogs_class.return_value = mock_discogs_instance

    sync = discogs_sync()
    username = "testuser"

    # Act
    sync.sync_library(username=username)

    # Assert
    mock_discogs_instance.get_user_collection.assert_called_once_with(username)
    mock_local_library.return_value.sync_discogs_json.assert_called_once_with({'releases': []})

@patch('builtins.open', new_callable=mock_open, read_data='discogs:\n  token: fake_token\n  username: configuser')
@patch('yaml.safe_load')
@patch('vinyl_dashboard.utils.discogs_sync.discogs')
@patch('vinyl_dashboard.utils.discogs_sync.LocalLibrary')
def test_sync_library_from_config(mock_local_library, mock_discogs_class, mock_safe_load, mock_open_file):
    # Arrange
    mock_config = {'discogs': {'token': 'fake_token', 'username': 'configuser'}}
    mock_safe_load.return_value = mock_config

    mock_discogs_instance = MagicMock()
    mock_discogs_instance.get_user_collection.return_value = {'releases': []}
    mock_discogs_class.return_value = mock_discogs_instance

    sync = discogs_sync()

    # Act
    sync.sync_library()

    # Assert
    mock_discogs_instance.get_user_collection.assert_called_once_with('configuser')
    mock_local_library.return_value.sync_discogs_json.assert_called_once_with({'releases': []})