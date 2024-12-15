import pygame
from mutagen.mp3 import MP3


class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        self.current_file = None

    def load(self, audio_file):
        pygame.mixer.music.load(audio_file)
        self.current_file = audio_file

    def play(self):
        pygame.mixer.music.play()
        self.is_playing = True

    def pause(self):
        pygame.mixer.music.pause()
        self.is_playing = False

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def get_pos(self):
        if not self.is_playing:
            return 0
        return pygame.mixer.music.get_pos() / 1000.0

    def get_duration(self):
        if self.current_file:
            audio = MP3(self.current_file)
            return audio.info.length
        return 0
