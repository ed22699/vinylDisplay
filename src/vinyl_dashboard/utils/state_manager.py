from enum import Enum, auto
from time import sleep
from utils.discogs_sync import discogs_sync
from audio.recorder import Recorder

class SystemState(Enum):
    INITIALISATION = auto()
    LISTENING = auto()
    FINDING = auto()
    DISPLAY = auto()

class state_manager:
    def __init__(self):
        # self.state = SystemState.INITIALISATION
        # NOTE: starting in listening state for testing purposes
        self.state = SystemState.LISTENING
        self.song_info = None
        self.timestamp = None
    
    def run(self):
        while True:
            if self.state == SystemState.INITIALISATION:
                self.__handle_initialisation()
            elif self.state == SystemState.LISTENING:
                self.__handle_listening()
            elif self.state == SystemState.FINDING:
                self.__handle_finding()
            elif self.state == SystemState.DISPLAY:
                self.__handle_display()
    
    def __handle_initialisation(self):
        sync = discogs_sync()
        sync.sync_library()
        self.state = SystemState.LISTENING
        print("Initialisation complete")

    def __handle_listening(self):
        recorder = Recorder()
        self.song_info = recorder.get_song()

        if self.song_info:
            print(f"Song detected, info: {self.song_info}")
            self.state = SystemState.FINDING
            self.timestamp = recorder.get_timestamp()
        else:
            print("No song detected, continuing to listen...")
            sleep(10)

    def __handle_finding(self):
        pass

    def __handle_display(self):
        pass