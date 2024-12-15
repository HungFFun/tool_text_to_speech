from openai import OpenAI
import os
import time
import subprocess


class TTSEngine:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.output_dir = os.path.abspath("output")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_speech(self, text, voice="alloy", settings=None):
        try:
            # Tạo tên file duy nhất dựa trên timestamp
            output_file = os.path.join(
                self.output_dir, f"speech_{int(time.time())}.mp3"
            )

            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=settings.get("pitch", 1.0) if settings else 1.0,
            )

            # Lưu file audio
            response.stream_to_file(output_file)
            return output_file

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")

    def combine_audio_files(self, audio_files):
        """Ghép nhiều file audio thành một file duy nhất sử dụng ffmpeg"""
        try:
            output_file = os.path.join(
                self.output_dir, f"combined_{int(time.time())}.mp3"
            )

            # Tạo file danh sách các audio files với đường dẫn tuyệt đối
            list_file = os.path.join(self.output_dir, "files.txt")
            with open(list_file, "w") as f:
                for audio_file in audio_files:
                    # Chuyển đổi sang đường dẫn tuyệt đối
                    abs_path = os.path.abspath(audio_file)
                    f.write(f"file '{abs_path}'\n")

            # Sử dụng ffmpeg để ghép các file
            cmd = [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file,
                "-c",
                "copy",
                output_file,
            ]

            # Thêm logging để debug
            print(f"Command: {' '.join(cmd)}")
            print(f"Content of {list_file}:")
            with open(list_file, "r") as f:
                print(f.read())

            subprocess.run(cmd, check=True)

            # Xóa file danh sách
            os.remove(list_file)

            # Xóa các file tạm
            for file in audio_files:
                try:
                    os.remove(file)
                except:
                    pass

            return output_file

        except Exception as e:
            raise Exception(f"Error combining audio files: {str(e)}")
