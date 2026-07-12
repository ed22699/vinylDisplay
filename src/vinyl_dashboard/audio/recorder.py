import yaml
import time
import audioop
import pyaudio
import wave
from vinyl_dashboard.api.audd_client import AudDClient

class Recorder:
    """
    Listens to audio input and uses the AUdD API to determine the song
    """
    def __init__(self, wav_path="data/recorded_snippet.wav"):
        """
        Instantiate the recorder and setup the AudDClient

        Args:
            wav_path (`string`, *optional*, defaults to `data/recorded_snipped.wav`):
                The path where the recorded audio snipped will be saved
        """
        self.timestamp = None

        # Token setup
        with open('config/config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        token = config['audd']['api_token']
        self.audd_client = AudDClient(token)

        # Audio configuration matching what AudD prefers
        self.p = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk_size = config['audio']['chunk_size']
        
        # Audio threshold settings
        self.ambient_threshold = config['audio']['ambient_threshold']
        self.record_seconds = config['audio']['record_seconds']       # Snippet length for AudD
        self.output_filename = wav_path

    def listen(self):
        """
        Listens to the audio input. When it detects volume above the 
        ambient threshold, it records a snippet and saves it to a file before using 
        it to query the AudD API for song recognition

        Returns:
            dict: Information about the identified song
        """

        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("Listening for music...")
        
        try:
            while True:
                # Read a small fragment of live audio
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                
                # audioop.rms calculates the average volume intensity of this chunk
                rms = audioop.rms(data, 2)  # 2 because paInt16 is 2 bytes per sample
                
                # If volume spikes past ambient room noise, assume a track started
                if rms > self.ambient_threshold:
                    print(f"🎵 Sound detected! (Volume: {rms}). Recording snippet...")
                    
                    # Stop listening to the live thread stream and lock down to record
                    stream.stop_stream()
                    stream.close()
                    
                    # Record the fixed-length sample block
                    self.timestamp = time.time()  # Capture the timestamp of when the song was detected
                    self.__record_audio_snippet()
                    
                    # Identify the song using the recorded snippet
                    return self.audd_client.recognize_song(self.output_filename)
                    
                # Short sleep prevents this while loop from maxing out your CPU core
                time.sleep(0.05)
                
        except Exception as e:
            print(f"Error in audio listener loop: {e}")
            if 'stream' in locals() and stream.is_active():
                stream.close()
            return None

    def __record_audio_snippet(self):
        """Internal helper to capture a distinct chunk of sound to disk."""
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        frames = []
        # Calculate exactly how many chunks match our target duration
        for _ in range(0, int(self.rate / self.chunk_size * self.record_seconds)):
            data = stream.read(self.chunk_size, exception_on_overflow=False)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        print("Recording finished. Writing to file.")
        
        # Save payload out as a standard WAV file
        with wave.open(self.output_filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))
    
    def get_timestamp(self):
        """
        Get a timestamp of when the audio was recorded
        
        Returns:
            float: The timestamp of when the song was detected
        """
        return self.timestamp