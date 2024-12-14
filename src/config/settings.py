import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio Configuration
AUDIO_OUTPUT_DIR = "resources/audio"
SUPPORTED_VOICES = {
    "Alloy": "alloy",
    "Echo": "echo",
    "Fable": "fable",
    "Onyx": "onyx",
    "Nova": "nova",
    "Shimmer": "shimmer",
}

# GUI Configuration
WINDOW_TITLE = "OpenAI Text To Speech"
WINDOW_SIZE = "600x500"
