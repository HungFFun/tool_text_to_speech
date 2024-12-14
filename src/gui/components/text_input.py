import tkinter as tk
from tkinter import ttk


class TextInput(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Label
        self.label = ttk.Label(self, text="Enter text to convert:")
        self.label.pack(pady=5)

        # Text area
        self.text_area = tk.Text(self, height=10, width=50)
        self.text_area.pack(pady=5)

    def get_text(self):
        return self.text_area.get("1.0", tk.END).strip()

    def clear(self):
        self.text_area.delete("1.0", tk.END)
