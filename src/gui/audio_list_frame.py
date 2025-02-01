import tkinter as tk
from tkinter import ttk
import pygame
from src.core.audio_merger import AudioMerger

class AudioListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.audio_merger = AudioMerger()
        self.audio_files = []
        
        # Title Label
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(
            title_frame,
            text="🎵 Audio Chunks",
            style="Header.TLabel"
        ).pack(side=tk.LEFT)
        
        # Create main container with border
        self.main_container = ttk.Frame(self, style="Dark.TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create listbox with scrollbar
        list_frame = ttk.Frame(self.main_container)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox with better styling
        self.listbox = tk.Listbox(
            list_frame,
            width=70,
            height=15,
            bg="#2D2D2D",
            fg="#FFFFFF",
            selectbackground="#0D7377",
            selectforeground="#FFFFFF",
            font=("Helvetica", 11),
            activestyle='none',
            yscrollcommand=scrollbar.set
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Controls frame
        controls_frame = ttk.Frame(self.main_container)
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Play button with icon
        self.play_btn = ttk.Button(
            controls_frame,
            text="▶ Play Selected",
            command=self.play_selected,
            style="Audio.TButton"
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_btn = ttk.Button(
            controls_frame,
            text="⏹ Stop",
            command=self.stop_playback,
            style="Audio.TButton"
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            controls_frame,
            text="Ready",
            style="Status.TLabel"
        )
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Initialize pygame mixer
        pygame.mixer.init()
    
    def add_audio(self, audio_path):
        self.audio_files.append(audio_path)
        # Format filename nicely
        filename = audio_path.split("/")[-1]
        chunk_num = len(self.audio_files)
        display_text = f"Chunk {chunk_num}: {filename}"
        self.listbox.insert(tk.END, display_text)
        self.audio_merger.add_audio(audio_path)
        
        # Auto-select first item if it's the only one
        if len(self.audio_files) == 1:
            self.listbox.selection_set(0)
    
    def play_selected(self):
        selection = self.listbox.curselection()
        if not selection:
            self.status_label.config(text="Please select an audio chunk")
            return
            
        selected_file = self.audio_files[selection[0]]
        try:
            pygame.mixer.music.load(selected_file)
            pygame.mixer.music.play()
            self.status_label.config(text="Playing...")
        except Exception as e:
            self.status_label.config(text="Error playing audio")
    
    def stop_playback(self):
        pygame.mixer.music.stop()
        self.status_label.config(text="Stopped") 