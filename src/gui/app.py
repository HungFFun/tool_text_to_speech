import tkinter as tk
from tkinter import ttk
from src.core.tts_engine import TTSEngine
from src.core.audio_player import AudioPlayer
import time
from src.gui.audio_list_frame import AudioListFrame


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text To Speech Converter")
        self.root.geometry("1000x800")

        # Color scheme
        self.bg_color = "#1E1E1E"  # Màu nền chính (xám đen)
        self.secondary_bg = "#2D2D2D"  # Màu nền phụ (xám nhạt hơn)
        self.text_color = "#FFFFFF"  # Màu chữ chính (trắng)
        self.accent_color = "#0D7377"  # Màu nhấn mạnh (xanh ngọc)
        self.hover_color = "#14FFEC"  # Màu hover (xanh sáng)
        self.label_color = "#CCCCCC"  # Màu chữ phụ (xám nhạt)
        self.border_color = "#323232"  # Màu viền (xám đậm)

        self.root.configure(bg=self.bg_color)

        self.tts_engine = TTSEngine()

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
            troughcolor=self.secondary_bg,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
        )

        # Frame styles
        style.configure("TFrame", background=self.bg_color)
        style.configure("Dark.TFrame", background=self.secondary_bg)

        # Label styles
        style.configure("TLabel", background=self.bg_color, foreground=self.label_color)

        style.configure(
            "Header.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Helvetica", 11, "bold"),
        )

        # Button styles
        style.configure(
            "TButton",
            background=self.secondary_bg,
            foreground=self.text_color,
            padding=5,
        )
        style.map(
            "TButton",
            background=[("active", self.accent_color)],
            foreground=[("active", self.text_color)],
        )

        # Convert button
        style.configure(
            "Convert.TButton",
            background=self.accent_color,
            padding=(30, 10),
            font=("Helvetica", 12, "bold"),
            relief="raised",
            borderwidth=0
        )
        style.map(
            "Convert.TButton",
            background=[("active", self.hover_color)],
            foreground=[("!active", self.text_color), ("active", self.bg_color)]
        )

        # Scale style
        style.configure(
            "Horizontal.TScale",
            background=self.bg_color,
            troughcolor=self.secondary_bg,
            bordercolor=self.border_color,
        )

        # Progressbar
        style.configure(
            "Horizontal.TProgressbar",
            background=self.accent_color,
            troughcolor=self.secondary_bg,
            bordercolor=self.border_color,
        )

        # Combobox
        style.configure(
            "TCombobox",
            fieldbackground=self.secondary_bg,
            background=self.text_color,
            foreground=self.text_color,
            arrowcolor=self.text_color,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.secondary_bg)],
            selectbackground=[("readonly", self.accent_color)],
            selectforeground=[("readonly", self.text_color)],
        )

        # LabelFrame styles
        style.configure(
            "Dark.TLabelframe",
            background=self.secondary_bg,
        )
        style.configure(
            "Dark.TLabelframe.Label",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Helvetica", 11, "bold"),
        )

        # Audio list styles
        style.configure(
            "Audio.TButton",
            background=self.secondary_bg,
            foreground=self.text_color,
            padding=(15, 8),
            font=("Helvetica", 10)
        )
        style.map(
            "Audio.TButton",
            background=[("active", self.accent_color)],
            foreground=[("active", self.text_color)]
        )
        
        style.configure(
            "Status.TLabel",
            background=self.secondary_bg,
            foreground=self.label_color,
            font=("Helvetica", 11)
        )

    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Text input area - takes full width at top
        self.setup_text_input(main_container)

        # Middle container for audio chunks and voice selection
        bottom_container = ttk.Frame(main_container)
        bottom_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Left side - Audio list (larger)
        audio_frame = ttk.Frame(bottom_container, style="Dark.TFrame")
        audio_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.audio_list = AudioListFrame(audio_frame)
        self.audio_list.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Right side - Voice selection (smaller)
        voice_frame = ttk.Frame(bottom_container)
        voice_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.setup_voice_selection(voice_frame)

        # Bottom section for convert button and status
        bottom_section = ttk.Frame(main_container)
        bottom_section.pack(fill=tk.X, pady=(10, 0))

        # Status bar (left side)
        self.status_label = ttk.Label(bottom_section, text="Ready", style="TLabel")
        self.status_label.pack(side=tk.LEFT)

        # Convert button (right side)
        convert_btn = ttk.Button(
            bottom_section,
            text="Convert to Speech",
            style="Convert.TButton",
            cursor="hand2",
            command=self.convert_to_speech,
        )
        convert_btn.pack(side=tk.RIGHT, padx=(0, 5))

    def setup_text_input(self, container):
        # Text input container with rounded corners
        text_frame = ttk.Frame(container)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas for rounded rectangle background
        self.canvas = tk.Canvas(
            text_frame, bg=self.bg_color, highlightthickness=0, bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Text area with increased height
        self.text_area = tk.Text(
            self.canvas,
            font=("Helvetica", 12),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            bg=self.secondary_bg,
            fg=self.text_color,
            insertbackground=self.text_color,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
            relief="flat",
            borderwidth=0,
            height=20,
        )

        # Info frame with better styling
        info_frame = ttk.Frame(text_frame, style="Dark.TFrame")
        info_frame.pack(fill=tk.X, padx=2, pady=(10, 2))  # Điều chỉnh padding ngoài

        # Add background for info frame
        info_bg = tk.Frame(
            info_frame,
            bg=self.secondary_bg,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        info_bg.pack(fill=tk.X, padx=0, pady=0)

        # Inner padding frame
        inner_frame = ttk.Frame(info_bg, style="Dark.TFrame")
        inner_frame.pack(fill=tk.X, padx=15, pady=10)

        # Tạo frame chứa tất cả các cột để căn giữa
        columns_container = ttk.Frame(inner_frame, style="Dark.TFrame")
        columns_container.pack(expand=True)

        # Column 1: Character and Word counts
        count_frame = ttk.Frame(columns_container, style="Dark.TFrame")
        count_frame.pack(side=tk.LEFT, padx=(0, 40))  # Tăng khoảng cách giữa các cột

        self.char_counter = ttk.Label(
            count_frame,
            text="Characters: 0/4,000",
            style="TLabel",
            background=self.secondary_bg,
        )
        self.char_counter.pack(anchor=tk.W, pady=(0, 5))

        self.word_count_label = ttk.Label(
            count_frame, text="Words: 0", style="TLabel", background=self.secondary_bg
        )
        self.word_count_label.pack(anchor=tk.W)

        # Column 2: Time estimates
        time_frame = ttk.Frame(columns_container, style="Dark.TFrame")
        time_frame.pack(side=tk.LEFT, padx=(0, 40))  # Tăng khoảng cách giữa các cột

        self.time_estimate_label = ttk.Label(
            time_frame,
            text="Est. Time: 0s",
            style="TLabel",
            background=self.secondary_bg,
        )
        self.time_estimate_label.pack(anchor=tk.W, pady=(0, 5))

        self.actual_time_label = ttk.Label(
            time_frame, text="Actual: --", style="TLabel", background=self.secondary_bg
        )
        self.actual_time_label.pack(anchor=tk.W)

        # Column 3: Cost estimates
        cost_frame = ttk.Frame(columns_container, style="Dark.TFrame")
        cost_frame.pack(side=tk.LEFT)

        self.cost_estimate_label = ttk.Label(
            cost_frame,
            text="Est. Cost: $0.0000",
            style="TLabel",
            background=self.secondary_bg,
        )
        self.cost_estimate_label.pack(anchor=tk.W, pady=(0, 5))

        self.actual_cost_label = ttk.Label(
            cost_frame, text="Actual: --", style="TLabel", background=self.secondary_bg
        )
        self.actual_cost_label.pack(anchor=tk.W)

        # Function to draw rounded rectangle
        def draw_rounded_corners(event=None):
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            radius = 15

            self.canvas.delete("all")
            self.canvas.create_polygon(
                radius,
                0,
                width - radius,
                0,
                width,
                0,
                width,
                radius,
                width,
                height - radius,
                width,
                height,
                width - radius,
                height,
                radius,
                height,
                0,
                height,
                0,
                height - radius,
                0,
                radius,
                0,
                0,
                smooth=True,
                fill=self.secondary_bg,
                outline=self.border_color,
            )

            self.text_area.place(x=0, y=0, width=width, height=height - 40)
            info_frame.lift()

        self.canvas.bind("<Configure>", draw_rounded_corners)

        # Bind text change events
        self.text_area.bind("<KeyRelease>", self.update_text_info)
        self.text_area.bind("<KeyPress>", self.update_text_info)

        # Default text
        self.text_area.insert("1.0", "Enter your text here...")
        self.text_area.bind("<FocusIn>", self.clear_default_text)
        self.text_area.bind("<FocusOut>", self.restore_default_text)

    def setup_voice_selection(self, container):
        # Voice selection container with rounded corners
        voice_container = ttk.Frame(container)
        voice_container.pack(fill=tk.BOTH, pady=5)

        # Create canvas for rounded rectangle background
        self.voice_canvas = tk.Canvas(
            voice_container, 
            bg=self.bg_color, 
            highlightthickness=0, 
            bd=0, 
            width=200,  # Fixed width for voice selection
            height=150
        )
        self.voice_canvas.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Main content frame
        voice_content = ttk.Frame(self.voice_canvas, style="Dark.TFrame")

        # Function to draw rounded rectangle
        def draw_rounded_corners(event=None):
            width = self.voice_canvas.winfo_width()
            height = self.voice_canvas.winfo_height()
            radius = 15

            self.voice_canvas.delete("all")
            self.voice_canvas.create_polygon(
                radius,
                0,
                width - radius,
                0,
                width,
                0,
                width,
                radius,
                width,
                height - radius,
                width,
                height,
                width - radius,
                height,
                radius,
                height,
                0,
                height,
                0,
                height - radius,
                0,
                radius,
                0,
                0,
                smooth=True,
                fill=self.secondary_bg,
                outline=self.border_color,
            )

            voice_content.place(x=15, y=15, width=width - 30, height=height - 30)

        self.voice_canvas.bind("<Configure>", draw_rounded_corners)

        # Title
        title_frame = ttk.Frame(voice_content, style="Dark.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(
            title_frame,
            text="🎤 Voice Selection",
            style="Header.TLabel",
            background=self.secondary_bg,
        ).pack(side=tk.LEFT)

        # Voice dropdown
        voice_frame = ttk.Frame(voice_content, style="Dark.TFrame")
        voice_frame.pack(fill=tk.X, pady=(0, 5))

        self.voice_var = tk.StringVar(value="Echo")
        voice_combo = ttk.Combobox(
            voice_frame,
            textvariable=self.voice_var,
            values=["Alloy", "Echo", "Fable", "Onyx", "Nova", "Shimmer"],
            state="readonly",
        )
        voice_combo.pack(fill=tk.X)

    def on_focus_in(self, event):
        if self.text_area.get("1.0", "end-1c") == "Enter your text here...":
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg=self.text_color)

    def on_focus_out(self, event):
        if not self.text_area.get("1.0", "end-1c"):
            self.text_area.insert("1.0", "Enter your text here...")
            self.text_area.config(fg=self.label_color)

    def format_price(self, price):
        """Format giá tiền với 4 chữ số thập phân"""
        return f"${price:.4f}"

    def format_time(self, seconds):
        """Format thời gian sang dạng mm:ss hoặc hh:mm:ss"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = seconds % 60
            return f"{minutes}m {seconds:.1f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = seconds % 60
            return f"{hours}h {minutes}m {seconds:.1f}s"

    def format_number(self, number):
        """Format số với dấu phẩy ngăn cách hàng nghìn"""
        return f"{number:,}"

    def update_text_info(self, event=None):
        """Cập nhật thông tin về text khi có thay đổi"""
        text = self.text_area.get("1.0", tk.END).strip()
        if text == "Enter your text here...":
            return

        # Đếm ký tự
        char_count = len(text)
        formatted_char_count = self.format_number(char_count)
        self.char_counter.config(text=f"Characters: {formatted_char_count}/4,000")
        if char_count > 4000:
            self.char_counter.config(foreground="#FF4444")
        else:
            self.char_counter.config(foreground=self.label_color)

        # Đếm từ
        words = text.split()
        word_count = len(words)
        formatted_word_count = self.format_number(word_count)
        self.word_count_label.config(text=f"Words: {formatted_word_count}")

        # Ước tính thời gian
        est_time = round(word_count / 3)  # Rough estimate: ~3 words per second
        formatted_est_time = self.format_time(est_time)
        self.time_estimate_label.config(text=f"Est. Time: {formatted_est_time}")

        # Ước tính chi phí
        # OpenAI TTS pricing: $0.015 per 1,000 characters
        estimated_cost = (char_count / 1000) * 0.015
        formatted_cost = self.format_price(estimated_cost)
        self.cost_estimate_label.config(text=f"Est. Cost: {formatted_cost}")

        # Reset actual values
        self.actual_time_label.config(text="Actual: --")
        self.actual_cost_label.config(text="Actual: --")

    def update_conversion_progress(self, completed, total):
        """Callback để cập nhật tiến trình"""
        percentage = (completed / total) * 100
        self.status_label.config(
            text=f"Converting... {completed}/{total} chunks ({percentage:.1f}%)"
        )
        self.root.update()

    def convert_to_speech(self):
        try:
            text = self.text_area.get("1.0", tk.END).strip()
            if not text or text == "Enter your text here...":
                self.status_label.config(text="Please enter some text!")
                return

            self.status_label.config(text="Starting conversion...")
            self.root.update()

            start_time = time.time()
            voice = self.voice_var.get().lower()
            settings = {}

            def update_progress(completed, total):
                percentage = (completed / total) * 100
                self.status_label.config(
                    text=f"Converting... {completed}/{total} chunks ({percentage:.1f}%)"
                )
                self.root.update()

            self.tts_engine.set_progress_callback(update_progress)

            # Xử lý text và tạo audio
            audio_files = self.tts_engine.generate_speech_parallel(
                text, voice, settings
            )

            # Cập nhật thông tin
            end_time = time.time()
            actual_time = end_time - start_time
            formatted_time = self.format_time(actual_time)
            actual_cost = (len(text) / 1000) * 0.015
            formatted_cost = self.format_price(actual_cost)

            # Cập nhật actual time và cost
            self.actual_time_label.config(text=f"Actual: {formatted_time}")
            self.actual_cost_label.config(text=f"Actual: {formatted_cost}")

            self.status_label.config(
                text=f"Conversion completed! ({self.format_number(len(text))} characters in {formatted_time})"
            )

            # Add audio files to the list
            for audio_file in audio_files:
                self.audio_list.add_audio(audio_file)

        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def run(self):
        self.root.mainloop()

    def clear_default_text(self, event):
        """Xóa text mặc định khi focus vào text area"""
        if self.text_area.get("1.0", tk.END).strip() == "Enter your text here...":
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg=self.text_color)
            self.update_text_info()

    def restore_default_text(self, event):
        """Khôi phục text mặc định khi không có nội dung và mất focus"""
        if not self.text_area.get("1.0", tk.END).strip():
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", "Enter your text here...")
            self.text_area.config(fg=self.label_color)
            self.update_text_info()
