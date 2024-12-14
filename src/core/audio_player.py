import pygame


class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.current_file = None
        self.is_playing = False

    def load(self, audio_file: str):
        self.current_file = audio_file
        pygame.mixer.music.load(audio_file)

    def play(self):
        if self.current_file:
            if self.is_playing:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.is_playing = True

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
