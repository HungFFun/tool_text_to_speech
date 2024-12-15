from openai import OpenAI
import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


class TTSEngine:
    def __init__(self):
        self.output_dir = os.path.abspath("output")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.max_workers = 10
        self.max_retries = 3
        self.retry_delay = 1  # seconds

    def generate_speech_with_retry(self, text, voice="alloy", settings=None):
        for attempt in range(self.max_retries):
            try:
                return self.generate_speech(text, voice, settings)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay)

    def generate_speech(self, text, voice="alloy", settings=None):
        try:
            output_file = os.path.join(self.output_dir, f"speech_{int(time.time()*1000)}.mp3")
            
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=settings.get('pitch', 1.0) if settings else 1.0,
            )

            response.stream_to_file(output_file)
            return output_file

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")

    def generate_speech_parallel(self, chunks, voice="alloy", settings=None):
        audio_files = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_chunk = {
                executor.submit(self.generate_speech_with_retry, chunk, voice, settings): i 
                for i, chunk in enumerate(chunks)
            }

            completed = 0
            total = len(chunks)
            for future in as_completed(future_to_chunk):
                chunk_index = future_to_chunk[future]
                try:
                    audio_file = future.result()
                    completed += 1
                    audio_files.append((chunk_index, audio_file))
                    if self.progress_callback:
                        self.progress_callback(completed, total)
                except Exception as e:
                    raise Exception(f"Error processing chunk {chunk_index}: {str(e)}")

        audio_files.sort(key=lambda x: x[0])
        return [file for _, file in audio_files]

    def set_progress_callback(self, callback):
        self.progress_callback = callback

    def combine_audio_files(self, audio_files):
        """Ghép nhiều file audio thành một file duy nhất sử dụng ffmpeg"""
        try:
            output_file = os.path.join(self.output_dir, f"combined_{int(time.time())}.mp3")
            
            list_file = os.path.join(self.output_dir, "files.txt")
            with open(list_file, "w") as f:
                for audio_file in audio_files:
                    abs_path = os.path.abspath(audio_file)
                    f.write(f"file '{abs_path}'\n")

            # Thêm -loglevel error để ẩn các thông báo không cần thiết
            cmd = [
                'ffmpeg',
                '-loglevel', 'error',  # Chỉ hiển thị lỗi
                '-f', 'concat',
                '-safe', '0',
                '-i', list_file,
                '-c', 'copy',
                output_file
            ]
            
            # Chuyển hướng stdout và stderr
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Cleanup
            os.remove(list_file)
            for file in audio_files:
                try:
                    os.remove(file)
                except:
                    pass

            return output_file

        except Exception as e:
            raise Exception(f"Error combining audio files: {str(e)}")
