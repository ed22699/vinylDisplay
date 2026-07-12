import requests

class AudDClient:
    """
    API client for interacting with the AudD API
    """
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.audd.io/"

    def recognize_song(self, audio_file_path):
        """
        Recognize a song using the AudD API.

        Args:
            audio_file_path (`str`): 
                Path to the audio file to be recognized.

        Returns:
            JSON response from the AudD API.
        """

        with open(audio_file_path, 'rb') as audio_file:
            files = {'file': audio_file}
            data = {'api_token': self.api_token}
            response = requests.post(f"{self.base_url}recognize", files=files, data=data)
        
        if response.status_code != 200:
            # TODO: Implement logging and do not raise an exception, handle error gracefully
            print(f"Error recognizing song: {response.status_code} - {response.text}")
            return None

        return response.json()