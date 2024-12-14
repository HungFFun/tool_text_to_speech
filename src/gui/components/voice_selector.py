import tkinter as tk
from tkinter import ttk


class VoiceSelector(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.voices = {
            "Alloy": "alloy",
            "Echo": "echo",
            "Fable": "fable",
            "Onyx": "onyx",
            "Nova": "nova",
            "Shimmer": "shimmer",
        }
        self.setup_ui()

    def setup_ui(self):
        # Label
        self.label = ttk.Label(self, text="Select Voice:")
        self.label.pack(pady=5)

        # Combobox
        self.selected_voice = tk.StringVar()
        self.voice_combo = ttk.Combobox(
            self, textvariable=self.selected_voice, values=list(self.voices.keys())
        )
        self.voice_combo.set(list(self.voices.keys())[0])
        self.voice_combo.pack(pady=5)

    def get_selected_voice(self):
        return self.voices[self.selected_voice.get()]
