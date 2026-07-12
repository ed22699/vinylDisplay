import yaml
import time
from vinyl_dashboard.api.audd_client import AudDClient

class Recorder:
    """
    Listens to audio input and uses the AUdD API to determine the song
    """
    def __init__(self):
        """
        Instantiate the recorder and setup the AudDClient
        """
        self.path = None
        self.timestamp = None
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        token = config['audd']['api_token']
        self.audd_client = AudDClient(token)

    
    def listen(self):
        """
        Listens to the audio input and if it believes a song is being played it will record the audio 
        and send it to the AudD API for recognition
        
        Returns:
            dict: Information about the identified song
        """
        # If noise signals song then get record
        # NOTE: Don't risk api calls till we have learned how to do noise levels
        return None
        # song_info = self.__get_song()
        # return song_info

    def get_timestamp(self):
        """
        Get a timestamp of when the audio was recorded
        
        Returns:
            float: The timestamp of when the song was detected
        """
        return self.timestamp

    def __get_song(self):
        # Stamp point of listening
        self.timestamp = time.time() 

        # Record audio and save to self.path

        # Identify song
        response = self.audd_client.recognize_song(self.path)

        # Return song info
        return response