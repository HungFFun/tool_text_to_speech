import tkinter as tk
from src.gui.components.text_input import TextInput
from src.gui.components.voice_selector import VoiceSelector
from src.gui.components.control_panel import ControlPanel
from src.core.tts_engine import TTSEngine
from src.core.audio_player import AudioPlayer
from src.config.settings import WINDOW_TITLE, WINDOW_SIZE


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        # Initialize core components
        self.tts_engine = TTSEngine()
        self.audio_player = AudioPlayer()

        # Initialize GUI components
        self.text_input = TextInput(self.root)
        self.voice_selector = VoiceSelector(self.root)
        self.control_panel = ControlPanel(
            self.root, self.on_convert, self.on_play, self.on_pause
        )

        self.setup_layout()

    def setup_layout(self):
        """Setup the layout of GUI components"""
        self.text_input.pack(pady=10)
        self.voice_selector.pack(pady=5)
        self.control_panel.pack(pady=20)

    def on_convert(self):
        """Handle convert button click"""
        text = self.text_input.get_text()
        voice = self.voice_selector.get_selected_voice()

        try:
            audio_file = self.tts_engine.generate_speech(text, voice)
            self.audio_player.load(audio_file)
            self.control_panel.set_status("Conversion successful!", "green")
        except Exception as e:
            self.control_panel.set_status(f"Error: {str(e)}", "red")

    def on_play(self):
        """Handle play button click"""
        self.audio_player.play()

    def on_pause(self):
        """Handle pause button click"""
        if self.audio_player.is_playing:
            self.audio_player.pause()
        else:
            self.audio_player.resume()

    def run(self):
        """Start the application"""
        self.root.mainloop()
