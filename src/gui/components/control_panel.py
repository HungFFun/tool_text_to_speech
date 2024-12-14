import tkinter as tk
from tkinter import ttk


class ControlPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.on_convert = None
        self.on_play = None
        self.setup_ui()

    def setup_ui(self):
        # Buttons frame
        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(pady=10)

        # Convert button
        self.convert_btn = ttk.Button(
            self.buttons_frame, text="Convert to Speech", command=self._handle_convert
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)

        # Play button
        self.play_btn = ttk.Button(
            self.buttons_frame, text="Play", command=self._handle_play
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(pady=10)

    def _handle_convert(self):
        if self.on_convert:
            self.on_convert()

    def _handle_play(self):
        if self.on_play:
            self.on_play()

    def set_convert_callback(self, callback):
        self.on_convert = callback

    def set_play_callback(self, callback):
        self.on_play = callback

    def set_status(self, message, color="black"):
        self.status_label.config(text=message, foreground=color)
