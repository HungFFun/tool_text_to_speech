import tkinter as tk
from tkinter import ttk
from src.core.tts_engine import TTSEngine
from src.core.audio_player import AudioPlayer
import time


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text To Speech Converter")
        self.root.geometry("1000x800")

        # Set background color
        self.bg_color = "#000000"
        self.secondary_bg = "#1E1E1E"
        self.text_color = "#FFFFFF"
        self.accent_color = "#007ACC"

        self.root.configure(bg=self.bg_color)

        self.tts_engine = TTSEngine()
        self.audio_player = AudioPlayer()

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        # Configure colors
        style.configure(
            ".",
            background=self.bg_color,
            foreground=self.text_color,
        )

        style.configure(
            "TFrame",
            background=self.bg_color,
        )

        style.configure(
            "TLabel",
            background=self.bg_color,
            foreground=self.text_color,
        )

        style.configure(
            "TLabelframe",
            background=self.bg_color,
            foreground=self.text_color,
        )

        style.configure(
            "TLabelframe.Label",
            background=self.bg_color,
            foreground=self.text_color,
        )

        style.configure(
            "TButton",
            background=self.secondary_bg,
            foreground=self.text_color,
        )

        style.configure(
            "Convert.TButton",
            background=self.accent_color,
            foreground=self.text_color,
            padding=(30, 15),
            font=("Helvetica", 12, "bold"),
        )

        style.configure(
            "Horizontal.TScale",
            background=self.bg_color,
            troughcolor=self.secondary_bg,
        )

        style.configure(
            "Horizontal.TProgressbar",
            background=self.accent_color,
            troughcolor=self.secondary_bg,
        )

    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Content frame
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Text input area
        self.setup_text_input(left_panel)

        # Right panel
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))

        # Voice selection
        self.setup_voice_selection(right_panel)

        # Convert button
        convert_frame = ttk.Frame(main_container)
        convert_frame.pack(fill=tk.X, pady=20)

        convert_btn = ttk.Button(
            convert_frame,
            text="Convert to Speech",
            style="Convert.TButton",
            command=self.convert_to_speech,
        )
        convert_btn.pack(side=tk.RIGHT)

        # Audio player
        player_frame = ttk.LabelFrame(main_container, text="Audio Player")
        player_frame.pack(fill=tk.X, pady=(0, 10))
        self.setup_audio_player(player_frame)

        # Status bar
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)

    def setup_text_input(self, container):
        # Input container
        input_frame = ttk.Frame(container)
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Header frame
        header_frame = ttk.Frame(input_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))

        # Title with icon
        ttk.Label(
            header_frame, 
            text="✏️ Input Text"
        ).pack(side=tk.LEFT)

        # Character counter
        self.char_counter = ttk.Label(
            header_frame,
            text="0/4000"
        )
        self.char_counter.pack(side=tk.RIGHT)

        # Text area
        self.text_area = tk.Text(
            input_frame,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            padx=10,
            pady=10,
            bg=self.secondary_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
            relief="solid",
            borderwidth=1,
            height=12
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Info panel frame
        info_panel = ttk.Frame(input_frame)
        info_panel.pack(fill=tk.X, pady=(5, 0))
        
        # Left side info (Word count)
        left_info = ttk.Frame(info_panel)
        left_info.pack(side=tk.LEFT)
        
        self.word_count_label = ttk.Label(
            left_info, 
            text="Words: 0"
        )
        self.word_count_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Right side info (Time estimates)
        right_info = ttk.Frame(info_panel)
        right_info.pack(side=tk.RIGHT)
        
        self.time_estimate_label = ttk.Label(
            right_info, 
            text="Est. Time: 0s"
        )
        self.time_estimate_label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.actual_time_label = ttk.Label(
            right_info, 
            text="Actual: --"
        )
        self.actual_time_label.pack(side=tk.LEFT)

        # Bind events
        self.text_area.bind("<FocusIn>", self.on_focus_in)
        self.text_area.bind("<FocusOut>", self.on_focus_out)
        self.text_area.bind("<KeyRelease>", self.update_text_info)

    def setup_voice_selection(self, container):
        # Voice selection frame
        voice_frame = ttk.LabelFrame(container, text="Voice Selection")
        voice_frame.pack(fill=tk.X, pady=5)

        # Voice dropdown
        self.voice_var = tk.StringVar(value="Alloy")
        voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=["Alloy", "Echo", "Fable", "Onyx", "Nova", "Shimmer"],
            state="readonly",
        )
        voice_combo.pack(fill=tk.X, pady=5)

        # Voice settings
        settings_frame = ttk.Frame(voice_frame)
        settings_frame.pack(fill=tk.X, pady=5)

        # Pitch control
        ttk.Label(settings_frame, text="Pitch:").pack(side=tk.LEFT)
        self.pitch_var = tk.DoubleVar(value=1.0)
        pitch_scale = ttk.Scale(
            settings_frame,
            from_=0.5,
            to=2.0,
            orient="horizontal",
            variable=self.pitch_var,
            command=self.update_pitch,
        )
        pitch_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.pitch_label = ttk.Label(settings_frame, text="1.0")
        self.pitch_label.pack(side=tk.LEFT)

        # Stability control
        stability_frame = ttk.Frame(voice_frame)
        stability_frame.pack(fill=tk.X, pady=5)

        ttk.Label(stability_frame, text="Stability:").pack(side=tk.LEFT)
        self.stability_var = tk.DoubleVar(value=0.5)
        stability_scale = ttk.Scale(
            stability_frame,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            variable=self.stability_var,
            command=self.update_stability,
        )
        stability_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.stability_label = ttk.Label(stability_frame, text="0.5")
        self.stability_label.pack(side=tk.LEFT)

        # Clarity control
        clarity_frame = ttk.Frame(voice_frame)
        clarity_frame.pack(fill=tk.X, pady=5)

        ttk.Label(clarity_frame, text="Clarity:").pack(side=tk.LEFT)
        self.clarity_var = tk.DoubleVar(value=0.5)
        clarity_scale = ttk.Scale(
            clarity_frame,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            variable=self.clarity_var,
            command=self.update_clarity,
        )
        clarity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.clarity_label = ttk.Label(clarity_frame, text="0.5")
        self.clarity_label.pack(side=tk.LEFT)

    def setup_audio_player(self, container):
        # Controls frame
        controls_frame = ttk.Frame(container)
        controls_frame.pack(fill=tk.X, padx=10, pady=5)

        # Play button
        self.play_btn = ttk.Button(controls_frame, text="▶", command=self.play_audio)
        self.play_btn.pack(side=tk.LEFT, padx=2)

        # Pause button
        self.pause_btn = ttk.Button(controls_frame, text="⏸", command=self.pause_audio)
        self.pause_btn.pack(side=tk.LEFT, padx=2)

        # Stop button
        self.stop_btn = ttk.Button(controls_frame, text="⏹", command=self.stop_audio)
        self.stop_btn.pack(side=tk.LEFT, padx=2)

        # Progress frame
        progress_frame = ttk.Frame(container)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.current_time = ttk.Label(progress_frame, text="0:00")
        self.current_time.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(
            progress_frame, mode="determinate", length=300
        )
        self.progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.total_time = ttk.Label(progress_frame, text="0:00")
        self.total_time.pack(side=tk.RIGHT)

        # Volume frame
        volume_frame = ttk.Frame(container)
        volume_frame.pack(fill=tk.X, padx=10, pady=5)

        volume_icon = ttk.Label(volume_frame, text="🔊")
        volume_icon.pack(side=tk.LEFT, padx=(0, 5))

        self.volume_var = tk.DoubleVar(value=100)
        self.volume_slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.volume_var,
            command=self.update_volume,
        )
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.volume_label = ttk.Label(volume_frame, text="100%")
        self.volume_label.pack(side=tk.LEFT, padx=5)

    def on_focus_in(self, event):
        if self.text_area.get("1.0", "end-1c") == "Enter your text here...":
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg=self.text_color)

    def on_focus_out(self, event):
        if not self.text_area.get("1.0", "end-1c"):
            self.text_area.insert("1.0", "Enter your text here...")
            self.text_area.config(fg="#666666")

    def update_text_info(self, event=None):
        text = self.text_area.get("1.0", tk.END).strip()
        if text == "Enter your text here...":
            return
            
        # Update character count
        char_count = len(text)
        self.char_counter.config(text=f"{char_count}/4000")
        if char_count > 4000:
            self.char_counter.config(foreground="#FF4444")
        else:
            self.char_counter.config(foreground=self.text_color)

        # Update word count
        words = text.split()
        word_count = len(words)
        self.word_count_label.config(text=f"Words: {word_count}")

        # Update time estimate (rough estimate: ~3 words per second)
        est_time = round(word_count / 3)
        self.time_estimate_label.config(text=f"Est. Time: {est_time}s")

    def update_pitch(self, value):
        self.pitch_label.config(text=f"{float(value):.1f}")

    def update_stability(self, value):
        self.stability_label.config(text=f"{float(value):.1f}")

    def update_clarity(self, value):
        self.clarity_label.config(text=f"{float(value):.1f}")

    def convert_to_speech(self):
        try:
            text = self.text_area.get("1.0", tk.END).strip()
            if not text or text == "Enter your text here...":
                self.status_label.config(text="Please enter some text!")
                return

            self.status_label.config(text="Converting...")
            self.root.update()

            voice = self.voice_var.get().lower()
            settings = {
                "pitch": self.pitch_var.get(),
                "stability": self.stability_var.get(),
                "clarity": self.clarity_var.get(),
            }

            audio_file = self.tts_engine.generate_speech(text, voice, settings)
            self.audio_player.load(audio_file)
            self.status_label.config(text="Conversion completed!")
            self.update_audio_progress()

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def play_audio(self):
        try:
            self.audio_player.play()
            self.status_label.config(text="Playing audio...")
            self.update_audio_progress()
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def pause_audio(self):
        try:
            self.audio_player.pause()
            self.status_label.config(text="Audio paused")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def stop_audio(self):
        try:
            self.audio_player.stop()
            self.progress_bar["value"] = 0
            self.current_time.config(text="0:00")
            self.status_label.config(text="Audio stopped")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def update_volume(self, value):
        try:
            volume = float(value) / 100
            self.audio_player.set_volume(volume)
            self.volume_label.config(text=f"{int(float(value))}%")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def update_audio_progress(self):
        if self.audio_player.is_playing:
            current_pos = self.audio_player.get_pos()
            duration = self.audio_player.get_duration()

            if duration > 0:
                progress = (current_pos / duration) * 100
                self.progress_bar["value"] = progress

                current_min = int(current_pos // 60)
                current_sec = int(current_pos % 60)
                total_min = int(duration // 60)
                total_sec = int(duration % 60)

                self.current_time.config(text=f"{current_min}:{current_sec:02d}")
                self.total_time.config(text=f"{total_min}:{total_sec:02d}")

            self.root.after(100, self.update_audio_progress)

    def run(self):
        self.root.mainloop()
