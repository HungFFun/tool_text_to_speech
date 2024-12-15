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
        self.root.configure(bg="#f0f0f0")

        self.tts_engine = TTSEngine()
        self.audio_player = AudioPlayer()

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()

        # Main styles
        style.configure("Custom.TButton", font=("Helvetica", 10), padding=10)

        # Convert button style
        style.configure(
            "Convert.TButton", font=("Helvetica", 12, "bold"), padding=(30, 15)
        )

        # Audio player styles
        style.configure("Player.TButton", font=("Arial", 12), padding=5, width=3)

        # Label styles
        style.configure(
            "Small.TLabel", font=("Arial", 9), foreground="#666666", padding=(5, 0)
        )

        style.configure(
            "Status.TLabel", font=("Arial", 9), foreground="#666666", padding=5
        )

        # Progress bar style
        style.configure(
            "Horizontal.TProgressbar",
            thickness=6,
            troughcolor="#E0E0E0",
            background="#2196F3",
        )

        # Scale style
        style.configure("Horizontal.TScale", sliderthickness=15, troughcolor="#E0E0E0")

        # LabelFrame style
        style.configure("TLabelframe", 
            padding=10,
            borderwidth=1,
            relief="solid",
            background="#FFFFFF"
        )
        
        style.configure(
            "TLabelframe.Label", 
            font=("Helvetica", 10), 
            foreground="#666666",
            background="#FFFFFF"
        )
        
        style.configure("TLabelframe.Border", 
            bordercolor="#E0E0E0"
        )

        # Input frame style
        style.configure(
            "Input.TFrame",
            background="#FFFFFF",
            relief="solid",
            borderwidth=1,
            bordercolor="#E0E0E0"  # Thêm màu border
        )
        
        # Input title style
        style.configure(
            "InputTitle.TLabel",
            font=("Helvetica", 12, "bold"),
            foreground="#333333",
            padding=(0, 0, 10, 0),
            background="#FFFFFF"
        )
        
        # Counter style
        style.configure(
            "Counter.TLabel",
            font=("Helvetica", 10),
            foreground="#666666",
            background="#FFFFFF"
        )
        
        # Info panel style
        style.configure(
            "InfoPanel.TFrame",
            background="#F8F9FA",
            relief="solid",
            borderwidth=1,
            bordercolor="#E0E0E0"  # Thêm màu border
        )
        
        # Info label style
        style.configure(
            "Info.TLabel",
            font=("Helvetica", 9),
            foreground="#666666",
            background="#F8F9FA"
        )

        # Frame style
        style.configure(
            "TFrame",
            borderwidth=0,
            background="#f0f0f0"
        )

    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # === Layer 2: Main Content ===
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel (70% width)
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Text input area in left panel
        self.setup_text_input(left_panel)

        # Right panel (30% width)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(10, 0))

        # Voice selection in right panel
        self.setup_voice_selection(right_panel)

        # Additional settings frame
        settings_frame = ttk.LabelFrame(right_panel, text="Settings", padding=10)
        settings_frame.pack(fill=tk.X, pady=10)

        # Speed control
        speed_frame = ttk.Frame(settings_frame)
        speed_frame.pack(fill=tk.X, pady=5)

        ttk.Label(speed_frame, text="Speed:", style="Small.TLabel").pack(
            side=tk.LEFT, padx=5
        )

        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(
            speed_frame,
            from_=0.5,
            to=2.0,
            orient="horizontal",
            variable=self.speed_var,
            command=self.update_speed,
        )
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.speed_label = ttk.Label(speed_frame, text="1.0x", style="Small.TLabel")
        self.speed_label.pack(side=tk.LEFT, padx=5)

        # === Layer 3: Convert Button ===
        convert_frame = ttk.Frame(main_container)
        convert_frame.pack(fill=tk.X, pady=20)

        self.setup_convert_button(convert_frame)

        # === Layer 4: Audio Player ===
        player_container = ttk.LabelFrame(
            main_container, text="Audio Player", padding=10
        )
        player_container.pack(fill=tk.X, pady=(0, 10))

        self.setup_audio_player(player_container)

        # === Layer 5: Status Bar ===
        status_frame = ttk.Frame(main_container)
        status_frame.pack(fill=tk.X, pady=(10, 0))

        self.status_label = ttk.Label(status_frame, text="Ready", style="Status.TLabel")
        self.status_label.pack(side=tk.LEFT)

    def setup_text_input(self, container):
        # Input frame with border and background
        input_frame = ttk.Frame(container, style="Input.TFrame")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Header frame
        header_frame = ttk.Frame(input_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT)

        ttk.Label(title_frame, text="✏️ Input Text", style="InputTitle.TLabel").pack(
            side=tk.LEFT
        )

        # Character counter in header
        self.char_counter = ttk.Label(
            header_frame, text="0/4000", style="Counter.TLabel"
        )
        self.char_counter.pack(side=tk.RIGHT)

        # Text area with custom styling
        self.text_area = tk.Text(
            input_frame,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            spacing1=2,  # Space between lines
            spacing2=2,  # Space between paragraphs
            selectbackground="#0078D7",
            selectforeground="white",
            bg="#FFFFFF",
            fg="#333333",
            insertbackground="#333333",  # Cursor color
            relief=tk.FLAT,
            height=12,
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Placeholder text
        self.placeholder_text = "Enter your text here..."
        self.text_area.insert("1.0", self.placeholder_text)
        self.text_area.config(fg="#999999")

        # Info panel frame
        info_panel = ttk.Frame(input_frame, style="InfoPanel.TFrame")
        info_panel.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Left side info (Word count)
        left_info = ttk.Frame(info_panel)
        left_info.pack(side=tk.LEFT)

        self.word_count_label = ttk.Label(
            left_info, text="Words: 0", style="Info.TLabel"
        )
        self.word_count_label.pack(side=tk.LEFT, padx=(0, 15))

        # Right side info (Time estimates)
        right_info = ttk.Frame(info_panel)
        right_info.pack(side=tk.RIGHT)

        self.time_estimate_label = ttk.Label(
            right_info, text="Est. Time: 0s", style="Info.TLabel"
        )
        self.time_estimate_label.pack(side=tk.LEFT, padx=(0, 15))

        self.actual_time_label = ttk.Label(
            right_info, text="Actual: --", style="Info.TLabel"
        )
        self.actual_time_label.pack(side=tk.LEFT)

        # Bind events
        self.text_area.bind("<FocusIn>", self.on_focus_in)
        self.text_area.bind("<FocusOut>", self.on_focus_out)
        self.text_area.bind("<KeyRelease>", self.update_text_info)

    def setup_voice_selection(self, container):
        voice_frame = ttk.LabelFrame(container, text="Voice Selection", padding=10)
        voice_frame.pack(fill=tk.X)

        # Voice selection
        self.voice_var = tk.StringVar(value="Alloy")
        voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=["Alloy", "Echo", "Fable", "Onyx", "Nova", "Shimmer"],
            state="readonly",
            width=20,
        )
        voice_combo.pack(fill=tk.X, padx=5, pady=5)

        # Voice settings frame
        settings_frame = ttk.Frame(voice_frame)
        settings_frame.pack(fill=tk.X, pady=5)

        # Pitch control
        pitch_frame = ttk.Frame(settings_frame)
        pitch_frame.pack(fill=tk.X, pady=2)

        ttk.Label(pitch_frame, text="Pitch:", style="Small.TLabel").pack(
            side=tk.LEFT, padx=5
        )

        self.pitch_var = tk.DoubleVar(value=1.0)
        pitch_scale = ttk.Scale(
            pitch_frame,
            from_=0.5,
            to=2.0,
            orient="horizontal",
            variable=self.pitch_var,
            command=self.update_pitch,
        )
        pitch_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.pitch_label = ttk.Label(pitch_frame, text="1.0", style="Small.TLabel")
        self.pitch_label.pack(side=tk.LEFT, padx=5)

        # Stability control
        stability_frame = ttk.Frame(settings_frame)
        stability_frame.pack(fill=tk.X, pady=2)

        ttk.Label(stability_frame, text="Stability:", style="Small.TLabel").pack(
            side=tk.LEFT, padx=5
        )

        self.stability_var = tk.DoubleVar(value=0.5)
        stability_scale = ttk.Scale(
            stability_frame,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            variable=self.stability_var,
            command=self.update_stability,
        )
        stability_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.stability_label = ttk.Label(
            stability_frame, text="0.5", style="Small.TLabel"
        )
        self.stability_label.pack(side=tk.LEFT, padx=5)

        # Clarity control
        clarity_frame = ttk.Frame(settings_frame)
        clarity_frame.pack(fill=tk.X, pady=2)

        ttk.Label(clarity_frame, text="Clarity:", style="Small.TLabel").pack(
            side=tk.LEFT, padx=5
        )

        self.clarity_var = tk.DoubleVar(value=0.5)
        clarity_scale = ttk.Scale(
            clarity_frame,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            variable=self.clarity_var,
            command=self.update_clarity,
        )
        clarity_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.clarity_label = ttk.Label(clarity_frame, text="0.5", style="Small.TLabel")
        self.clarity_label.pack(side=tk.LEFT, padx=5)

    def setup_convert_button(self, container):
        self.convert_btn = ttk.Button(
            container,
            text="Convert to Speech",
            style="Convert.TButton",
            command=self.convert_to_speech,
        )
        self.convert_btn.pack()

    def setup_audio_player(self, container):
        # === Control Buttons ===
        controls_frame = ttk.Frame(container)
        controls_frame.pack(pady=5)

        # Play button
        self.play_btn = ttk.Button(
            controls_frame, text="▶", style="Player.TButton", command=self.play_audio
        )
        self.play_btn.pack(side=tk.LEFT, padx=2)

        # Pause button
        self.pause_btn = ttk.Button(
            controls_frame, text="⏸", style="Player.TButton", command=self.pause_audio
        )
        self.pause_btn.pack(side=tk.LEFT, padx=2)

        # Stop button
        self.stop_btn = ttk.Button(
            controls_frame, text="⏹", style="Player.TButton", command=self.stop_audio
        )
        self.stop_btn.pack(side=tk.LEFT, padx=2)

        # === Progress Bar and Time ===
        progress_frame = ttk.Frame(container)
        progress_frame.pack(fill=tk.X, pady=(5, 0), padx=10)

        self.current_time = ttk.Label(progress_frame, text="0:00", style="Small.TLabel")
        self.current_time.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(
            progress_frame, mode="determinate", length=300
        )
        self.progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        self.total_time = ttk.Label(progress_frame, text="0:00", style="Small.TLabel")
        self.total_time.pack(side=tk.RIGHT)

        # === Volume Control ===
        volume_frame = ttk.Frame(container)
        volume_frame.pack(fill=tk.X, pady=5, padx=10)

        volume_icon = ttk.Label(volume_frame, text="🔊", style="Small.TLabel")
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

        self.volume_label = ttk.Label(volume_frame, text="100%", style="Small.TLabel")
        self.volume_label.pack(side=tk.LEFT, padx=5)

    def on_focus_in(self, event):
        if self.text_area.get("1.0", "end-1c") == self.placeholder_text:
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg="#333333")

    def on_focus_out(self, event):
        if not self.text_area.get("1.0", "end-1c"):
            self.text_area.insert("1.0", self.placeholder_text)
            self.text_area.config(fg="#999999")

    def update_text_info(self, event=None):
        # Skip update if placeholder text is showing
        if self.text_area.get("1.0", "end-1c") == self.placeholder_text:
            return

        # Get text content
        text = self.text_area.get("1.0", tk.END).strip()
        char_count = len(text)
        word_count = len(text.split())

        # Update character counter
        self.char_counter.config(text=f"{char_count}/4000")
        if char_count > 4000:
            self.char_counter.config(foreground="red")
        else:
            self.char_counter.config(foreground="#666666")

        # Update word count
        self.word_count_label.config(text=f"Words: {word_count}")

        # Calculate estimated time
        estimated_seconds = round(char_count / 150, 1)

        # Format estimated time string
        if estimated_seconds < 60:
            time_str = f"{estimated_seconds}s"
        else:
            minutes = int(estimated_seconds // 60)
            seconds = int(estimated_seconds % 60)
            time_str = f"{minutes}m {seconds}s"

        # Update time estimate
        self.time_estimate_label.config(text=f"Est. Time: {time_str}")

    def update_speed(self, value):
        speed = round(float(value), 1)
        self.speed_label.config(text=f"{speed}x")

    def update_pitch(self, value):
        pitch = round(float(value), 2)
        self.pitch_label.config(text=f"{pitch}")

    def update_stability(self, value):
        stability = round(float(value), 2)
        self.stability_label.config(text=f"{stability}")

    def update_clarity(self, value):
        clarity = round(float(value), 2)
        self.clarity_label.config(text=f"{clarity}")

    def convert_to_speech(self):
        try:
            text = self.text_area.get("1.0", tk.END).strip()
            if not text:
                self.status_label.config(text="Please enter some text!")
                return

            self.status_label.config(text="Converting...")
            self.root.update()

            # Record start time
            start_time = time.time()

            voice = self.voice_var.get().lower()
            settings = {
                "pitch": self.pitch_var.get(),
                "stability": self.stability_var.get(),
                "clarity": self.clarity_var.get(),
            }

            audio_file = self.tts_engine.generate_speech(text, voice, settings)
            self.audio_player.load(audio_file)

            # Calculate actual duration
            duration = self.audio_player.get_duration()
            if duration < 60:
                time_str = f"{duration:.1f}s"
            else:
                minutes = int(duration // 60)
                seconds = int(duration % 60)
                time_str = f"{minutes}m {seconds}s"

            self.actual_time_label.config(text=f"Actual: {time_str}")
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
