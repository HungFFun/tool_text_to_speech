import pygame
import os


class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.audio = None
        self.is_playing = False
        self.current_file = None

    def load(self, audio_file):
        try:
            if os.path.exists(audio_file):
                pygame.mixer.music.load(audio_file)
                self.current_file = audio_file
            else:
                raise FileNotFoundError("Audio file not found")
        except Exception as e:
            raise Exception(f"Error loading audio: {str(e)}")

    def play(self):
        try:
            if self.current_file:
                pygame.mixer.music.play()
                self.is_playing = True
            else:
                raise Exception("No audio file loaded")
        except Exception as e:
            raise Exception(f"Error playing audio: {str(e)}")

    def pause(self):
        try:
            pygame.mixer.music.pause()
            self.is_playing = False
        except Exception as e:
            raise Exception(f"Error pausing audio: {str(e)}")

    def stop(self):
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
        except Exception as e:
            raise Exception(f"Error stopping audio: {str(e)}")

    def set_volume(self, volume):
        try:
            pygame.mixer.music.set_volume(volume)
        except Exception as e:
            raise Exception(f"Error setting volume: {str(e)}")

    def get_pos(self):
        try:
            return pygame.mixer.music.get_pos() / 1000.0
        except Exception as e:
            return 0

    def get_duration(self):
        try:
            return 30  # Default duration
        except Exception as e:
            return 0

    def __del__(self):
        try:
            pygame.mixer.quit()
        except:
            pass
