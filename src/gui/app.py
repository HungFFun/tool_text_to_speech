import tkinter as tk
from tkinter import ttk, font
from src.core.tts_engine import TTSEngine
from src.core.audio_player import AudioPlayer
import time


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text To Speech Converter")
        self.root.geometry("800x800")
        self.root.configure(bg="#f0f0f0")  # Background color

        # Configure style
        self.setup_styles()

        # Initialize backend components
        self.tts_engine = TTSEngine()
        self.audio_player = AudioPlayer()

        self.setup_ui()

    def setup_styles(self):
        # Create custom styles
        style = ttk.Style()
        style.configure(
            "Header.TLabel", font=("Helvetica", 12, "bold"), foreground="#34495e"
        )

        style.configure("Stats.TLabel", font=("Helvetica", 10), foreground="#7f8c8d")

        style.configure("Custom.TButton", font=("Helvetica", 11), padding=10)

        style.configure("Custom.TFrame", background="#ffffff")

    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root, style="Custom.TFrame", padding="20")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Text Input Section - Removed title and label frame
        self.text_area = tk.Text(
            main_container,
            height=15,  # Increased height
            width=60,  # Increased width
            font=("Helvetica", 12),
            wrap=tk.WORD,
            bg="#ffffff",
            fg="#2c3e50",
            padx=15,  # Increased padding
            pady=15,
            relief="flat",  # Bỏ border bằng cách set relief='flat'
            highlightthickness=0,  # Bỏ highlight border khi focus
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=10)

        # Character Count Frame
        stats_frame = ttk.Frame(main_container)
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        self.char_count_label = ttk.Label(
            stats_frame, text="Characters: 0", style="Stats.TLabel"
        )
        self.char_count_label.pack(side=tk.LEFT, padx=5)

        ttk.Separator(stats_frame, orient=tk.VERTICAL).pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )

        self.word_count_label = ttk.Label(
            stats_frame, text="Words: 0", style="Stats.TLabel"
        )
        self.word_count_label.pack(side=tk.LEFT, padx=5)

        # Voice Selection Frame - Made more compact
        voice_frame = ttk.Frame(main_container)  # Changed from LabelFrame to Frame
        voice_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(
            voice_frame,
            text="Voice:",  # Shortened text
            style='Stats.TLabel'  # Changed to smaller font style
        ).pack(side=tk.LEFT, padx=5)

        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            width=20,  # Reduced width
            state='readonly'
        )
        self.voice_combo['values'] = ('Alloy', 'Echo', 'Fable', 'Onyx', 'Nova', 'Shimmer')
        self.voice_combo.current(0)
        self.voice_combo.pack(side=tk.LEFT, padx=5)

        # Conversion Stats Frame - Made more compact
        stats_container = ttk.Frame(main_container)  # Changed from LabelFrame to Frame
        stats_container.pack(fill=tk.X, pady=(0, 10))

        # First row: Process Time and Completion Time
        stats_row1 = ttk.Frame(stats_container)
        stats_row1.pack(fill=tk.X, pady=2)

        ttk.Label(
            stats_row1,
            text="Process:",  # Shortened text
            style='Stats.TLabel'
        ).pack(side=tk.LEFT, padx=5)

        self.conversion_time_label = ttk.Label(
            stats_row1,
            text="Not converted",
            style='Stats.TLabel'
        )
        self.conversion_time_label.pack(side=tk.LEFT, padx=5)

        ttk.Label(
            stats_row1,
            text="|",
            style='Stats.TLabel'
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(
            stats_row1,
            text="Completed:",  # Shortened text
            style='Stats.TLabel'
        ).pack(side=tk.LEFT, padx=5)

        self.current_time_label = ttk.Label(
            stats_row1,
            text="--:--:--",
            style='Stats.TLabel'
        )
        self.current_time_label.pack(side=tk.LEFT, padx=5)

        # Second row: Estimated Duration
        stats_row2 = ttk.Frame(stats_container)
        stats_row2.pack(fill=tk.X, pady=2)

        ttk.Label(
            stats_row2,
            text="Duration:",  # Shortened text
            style='Stats.TLabel'
        ).pack(side=tk.LEFT, padx=5)

        self.duration_label = ttk.Label(
            stats_row2,
            text="0 sec",
            style='Stats.TLabel'
        )
        self.duration_label.pack(side=tk.LEFT, padx=5)

        # Control Buttons Frame
        button_frame = ttk.Frame(main_container)
        button_frame.pack(pady=20)

        self.convert_btn = ttk.Button(
            button_frame,
            text="Convert to Speech",
            style="Custom.TButton",
            command=self.convert_to_speech,
        )
        self.convert_btn.pack(side=tk.LEFT, padx=5)

        self.play_btn = ttk.Button(
            button_frame,
            text="Play Audio",
            style="Custom.TButton",
            command=self.play_audio,
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)

        # Progress Frame
        progress_frame = ttk.Frame(main_container)
        progress_frame.pack(fill=tk.X, pady=(0, 10))

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            length=300,
            mode="determinate",
            style="Custom.Horizontal.TProgressbar",
        )
        self.progress_bar.pack(fill=tk.X)

        # Status Label
        self.status_label = ttk.Label(
            main_container, text="Ready", style="Stats.TLabel"
        )
        self.status_label.pack(pady=10)

        # Bind text changes to update character count
        self.text_area.bind("<KeyRelease>", self.update_counts)

    def update_counts(self, event=None):
        text = self.text_area.get("1.0", tk.END).strip()
        char_count = len(text)
        word_count = len(text.split())

        # Format character count with commas
        formatted_char_count = "{:,}".format(char_count)
        self.char_count_label.config(text=f"Characters: {formatted_char_count}")

        # Format word count with commas
        formatted_word_count = "{:,}".format(word_count)
        self.word_count_label.config(text=f"Words: {formatted_word_count}")

        # Calculate estimated duration in minutes and seconds
        estimated_seconds = word_count / 3
        minutes = int(estimated_seconds // 60)
        seconds = int(estimated_seconds % 60)

        if minutes > 0:
            duration_text = f"{minutes} min {seconds} sec"
        else:
            duration_text = f"{seconds} sec"

        self.duration_label.config(text=duration_text)

    def convert_to_speech(self):
        try:
            text = self.text_area.get("1.0", tk.END).strip()
            if not text:
                self.status_label.config(
                    text="Please enter some text!", foreground="#e74c3c"
                )
                return

            # Record start time
            start_time = time.time()

            self.progress_bar["value"] = 0
            self.status_label.config(text="Converting...", foreground="#3498db")
            self.root.update()

            voice = self.voice_var.get().lower()
            audio_file = self.tts_engine.generate_speech(text, voice)
            self.audio_player.load(audio_file)

            # Calculate processing time
            end_time = time.time()
            process_time = end_time - start_time

            # Format processing time
            minutes = int(process_time // 60)
            seconds = int(process_time % 60)
            milliseconds = int((process_time % 1) * 1000)

            if minutes > 0:
                time_text = f"{minutes}m {seconds}s {milliseconds}ms"
            else:
                time_text = f"{seconds}s {milliseconds}ms"

            self.conversion_time_label.config(text=time_text)

            # Update current time
            current_time = time.strftime("%H:%M:%S")
            self.current_time_label.config(text=f"Completed at: {current_time}")

            self.progress_bar["value"] = 100
            self.status_label.config(text="Conversion completed!", foreground="#27ae60")

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="#e74c3c")

    def play_audio(self):
        try:
            self.audio_player.play()
            self.status_label.config(text="Playing audio...", foreground="#3498db")
        except Exception as e:
            self.status_label.config(
                text=f"Error playing audio: {str(e)}", foreground="#e74c3c"
            )

    def run(self):
        self.root.mainloop()
