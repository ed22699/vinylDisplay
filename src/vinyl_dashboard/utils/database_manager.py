import sqlite3

class LocalLibrary:
    """
    Interact with the local database which holds the users record collection data
    """
    def __init__(self, db_path="data/collection.db"):
        """
        Instantiate instance of LocalLibrary and initialize the local database
        
        Args:
            db_path (`string`, *optional*, defaults to `data/collection.db`):
                The path to the local SQLite database file
        """
        self.db_path = db_path
        self.__init_db()

    def __init_db(self):
        """Creates the local cache table if it doesn't exist yet."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS collection (
                    discogs_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    cover_image TEXT
                )
            """)
            conn.commit()

    def sync_discogs_json(self, data):
        """
        Parses the raw Discogs JSON response dictionary 
        and updates the local database cache.

        Args:
            data (`dict`):
                The raw JSON response from the Discogs API containing the user's collection data
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("DELETE FROM collection")
            
            for release in data.get("releases", []):
                discogs_id = release.get("id")
                basic_info = release.get("basic_information", {})
                
                title = basic_info.get("title")
                cover_image = basic_info.get("cover_image")
                
                # Discogs nests artists in a list. We'll grab the first primary artist,
                # or fallback to 'Unknown Artist' if the list is empty.
                artists = basic_info.get("artists", [])
                artist = artists[0].get("name") if artists else "Unknown Artist"
                
                # INSERT OR REPLACE ensures that if an album cover changes or you re-sync,
                # it safely updates the entry instead of crashing on a duplicate ID error.
                cursor.execute("""
                    INSERT OR REPLACE INTO collection (discogs_id, title, artist, cover_image)
                    VALUES (?, ?, ?, ?)
                """, (discogs_id, title, artist, cover_image))
                
            conn.commit()
        print(f"Successfully synced {len(data.get('releases', []))} releases to the local database.")

    def lookup_album(self, album_title):
        """
        Checks if album is present in the local database

        Args:
            album_title (`string`):
                Title of the album to look up in the local database
        Returns:
            tuple: (title, artist, cover_image) if found, else None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # case-insensitive exact or close match lookup
            cursor.execute(
                "SELECT title, artist, cover_image FROM collection WHERE title LIKE ?", 
                (album_title,)
            )
            return cursor.fetchone() # Returns (title, artist, cover) or None