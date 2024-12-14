from openai import OpenAI
from src.config.settings import OPENAI_API_KEY, AUDIO_OUTPUT_DIR
import os
from datetime import datetime


class TTSEngine:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

    def generate_speech(self, text: str, voice: str) -> str:
        """
        Generate speech from text using OpenAI API
        Returns the path to the generated audio file
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(AUDIO_OUTPUT_DIR, f"speech_{timestamp}.mp3")

            response = self.client.audio.speech.create(
                model="tts-1", voice=voice, input=text
            )

            response.stream_to_file(output_file)
            return output_file

        except Exception as e:
            raise Exception(f"Speech generation failed: {str(e)}")
