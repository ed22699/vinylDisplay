import yaml
from vinyl_dashboard.api.discogs_client import discogs
from vinyl_dashboard.utils.database_manager import LocalLibrary

class discogs_sync:
    """
    Synchronizes the user's Discogs library with the local database
    """
    def __init__(self):
        """
        Initialize the Discogs synchronization utility
        """
        # Get token from config.yaml
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        token = config['discogs']['token']

        self.discogs_client = discogs(token)

    def sync_library(self, username = None):
        """
        Synchronizes the user's Discogs library with the local database
        
        Args:
            username (`string`, *optional*, defaults to `None`):
                The Discogs username for which to fetch the collection. **NOTE** If not provided username will be fetched from config file
            Returns:
                
        """
        # Get username from config if not provided
        if username is None:
            with open('config/config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            username = config['discogs']['username']

        # Fetch release data from Discogs
        library_data = self.discogs_client.get_user_collection(username)
        # Process and store the release data in the local database
        self.__store_library_data(library_data)

    def __store_library_data(self, library_data):
        # store cover_image, title, artists
        local_library = LocalLibrary()
        local_library.sync_discogs_json(library_data)
