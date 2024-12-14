import tkinter as tk
from tkinter import ttk
from src.gui.components.text_input import TextInput
from src.gui.components.voice_selector import VoiceSelector
from src.gui.components.control_panel import ControlPanel
from src.core.tts_engine import TTSEngine
from src.core.audio_player import AudioPlayer


class App:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Text To Speech Converter")
        self.root.geometry("600x500")

        # Create components
        self.text_input = TextInput(self.root)
        self.text_input.pack(pady=10, padx=20, fill=tk.X)

        self.voice_selector = VoiceSelector(self.root)
        self.voice_selector.pack(pady=10)

        self.control_panel = ControlPanel(self.root)
        self.control_panel.pack(pady=10)

        # Initialize backend components
        self.tts_engine = TTSEngine()
        self.audio_player = AudioPlayer()

        # Setup callbacks
        self.control_panel.set_convert_callback(self.on_convert)
        self.control_panel.set_play_callback(self.on_play)

    def on_convert(self):
        try:
            text = self.text_input.get_text()
            if not text:
                self.control_panel.set_status("Please enter some text!", "red")
                return

            voice = self.voice_selector.get_selected_voice()
            self.control_panel.set_status("Converting...", "blue")
            self.root.update()

            audio_file = self.tts_engine.generate_speech(text, voice)
            self.audio_player.load(audio_file)

            self.control_panel.set_status("Conversion successful!", "green")
        except Exception as e:
            self.control_panel.set_status(f"Error: {str(e)}", "red")

    def on_play(self):
        try:
            self.audio_player.play()
        except Exception as e:
            self.control_panel.set_status(f"Error playing audio: {str(e)}", "red")

    def run(self):
        self.root.mainloop()
