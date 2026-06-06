import requests

class discogs:
    """
    API client for interacting with the Discogs API
    """
    def __init__(self, token):
        """
        Initialize the Discogs API client
        
        
        Args:
            token (`string`):
                The Discogs API token
        """
        self.token = token
        self.base_url = "https://api.discogs.com"

    
    def get_user_collection(self, username):
        """
        Get the collection of albums and artists for a given Discogs username
        
        Args:
            username (`string`):
                The Discogs username for which to fetch the collection
            Returns:
                The response.json consisting of all the albums and artists present in the users discogs
        """
        # TODO : Implement pagination to fetch all pages if the collection is over 50 items
        url = f"{self.base_url}/users/{username}/collection/folders/0/releases"
        headers = {
            "Authorization": f"Discogs token={self.token}",
            "User-Agent": "VinylLiveDisplayProject/0.1 +https://github.com/ed22699/vinylDisplay" 
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching collection: {response.status_code} - {response.text}")

    # def get_release_details(self, release_id):
    #     url = f"{self.base_url}/releases/{release_id}"
    #     headers = {"Authorization": f"Discogs token={self.token}"}
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 200:
    #         return response.json()
    #     else:
    #         raise Exception(f"Error fetching release details: {response.status_code} - {response.text}")