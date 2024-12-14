import openai
import os
from pathlib import Path


class TTSEngine:
    def __init__(self):
        # Khởi tạo API key từ biến môi trường
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Tạo thư mục output nếu chưa tồn tại
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def generate_speech(self, text, voice, settings=None):
        try:
            if settings is None:
                settings = {"pitch": 1.0, "stability": 0.5, "clarity": 0.5}

            response = openai.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=settings.get("pitch", 1.0),
                # Các tham số khác có thể thêm vào tùy theo API hỗ trợ
            )

            output_file = self.output_dir / "output.mp3"
            response.stream_to_file(str(output_file))

            return str(output_file)

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")
