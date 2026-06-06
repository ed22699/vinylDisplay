import pytest
from unittest.mock import patch, MagicMock
from vinyl_dashboard.api.discogs_client import discogs

class TestDiscogsClient:
    @pytest.fixture
    def discogs_client(self):
        return discogs(token="fake_token")

    @patch('requests.get')
    def test_get_user_collection_success(self, mock_get, discogs_client):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 200
        expected_data = {"releases": [{"id": 123, "basic_information": {"title": "Test Album"}}]}
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response
        username = "testuser"

        # Act
        result = discogs_client.get_user_collection(username)

        # Assert
        mock_get.assert_called_once_with(
            f"https://api.discogs.com/users/{username}/collection/folders/0/releases",
            headers={
                "Authorization": f"Discogs token={discogs_client.token}",
                "User-Agent": "VinylLiveDisplayProject/0.1 +https://github.com/ed22699/vinylDisplay"
            }
        )
        assert result == expected_data

    @patch('requests.get')
    def test_get_user_collection_failure(self, mock_get, discogs_client):
        # Arrange
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        username = "nonexistentuser"

        # Act & Assert
        with pytest.raises(Exception, match="Error fetching collection: 404 - Not Found"):
            discogs_client.get_user_collection(username)
