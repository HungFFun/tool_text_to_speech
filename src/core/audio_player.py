import pygame

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_file = None
        self.is_playing = False

    def load(self, audio_file: str):
        """Load an audio file"""
        self.current_file = audio_file
        pygame.mixer.music.load(audio_file)

    def play(self):
        """Play the loaded audio file"""
        if self.current_file:
            pygame.mixer.music.play()
            self.is_playing = True

    def pause(self):
        """Pause the current playback"""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def resume(self):
        """Resume the paused playback"""
        if not self.is_playing:
            pygame.mixer.music.unpause()
            self.is_playing = True

    def stop(self):
        """Stop the current playback"""
        pygame.mixer.music.stop()
        self.is_playing = False