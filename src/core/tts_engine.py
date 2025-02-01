from openai import OpenAI
import os
import time
import subprocess
from queue import Queue
from threading import Thread
from datetime import datetime
import concurrent.futures


class TTSEngine:
    def __init__(self):
        self.output_dir = "output"  # Default output directory
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.max_workers = 15
        self.task_queue = Queue()
        self.result_queue = Queue()
        self.progress_callback = None

    def set_progress_callback(self, callback):
        """Set callback function để cập nhật tiến trình"""
        self.progress_callback = callback

    def generate_speech(self, text, voice="alloy", settings=None):
        """Tạo speech từ text"""
        try:
            # Sử dụng text làm input và trả về response
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=settings.get("pitch", 1.0) if settings else 1.0,
            )
            return response

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")

    def generate_speech_with_retry(
        self, chunk, voice="alloy", settings=None, max_retries=3
    ):
        """Thử lại khi gặp lỗi với exponential backoff"""
        for attempt in range(max_retries):
            try:
                return self.generate_speech(chunk, voice, settings)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                wait_time = (2**attempt) * 0.5  # 0.5s, 1s, 2s
                time.sleep(wait_time)

    def worker(self):
        """Worker thread để xử lý các task từ queue"""
        while True:
            task = self.task_queue.get()
            if task is None:
                break

            chunk_index, chunk, voice, settings = task
            try:
                audio_file = self.generate_speech_with_retry(chunk, voice, settings)
                self.result_queue.put((chunk_index, audio_file))
            except Exception as e:
                self.result_queue.put((chunk_index, None, str(e)))
            finally:
                self.task_queue.task_done()

    def optimize_chunk_size(self, text):
        """Tối ưu kích thước chunk"""
        optimal_size = 3500
        chunks = []
        current_chunk = ""
        sentences = text.replace("\n", ". ").split(". ")

        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= optimal_size:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def generate_speech_parallel(self, text, voice="echo", settings=None):
        # Create output directory if not exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        # Get current date for filename
        current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Split text into chunks
        chunks = self.optimize_chunk_size(text)
        audio_files = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            
            for i, chunk in enumerate(chunks):
                # Format filename with segment number and date
                output_path = os.path.join(
                    self.output_dir, 
                    f"segment_{i:03d}_{current_date}.mp3"
                )
                
                future = executor.submit(
                    self.convert_to_speech,  # Sử dụng convert_to_speech thay vì generate_speech
                    chunk,
                    output_path,
                    voice,
                    settings
                )
                futures.append(future)
                
            # Process results as they complete
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    audio_file = future.result()
                    audio_files.append(audio_file)
                    if self.progress_callback:
                        self.progress_callback(i + 1, len(chunks))
                except Exception as e:
                    print(f"Error processing chunk {i}: {str(e)}")
                    
        return sorted(audio_files)  # Return sorted to maintain order

    def combine_audio_files(self, audio_files):
        """Ghép nhiều file audio thành một file duy nhất"""
        try:
            output_file = os.path.join(
                self.output_dir, f"combined_{int(time.time())}.mp3"
            )

            list_file = os.path.join(self.output_dir, "files.txt")
            with open(list_file, "w") as f:
                for audio_file in audio_files:
                    abs_path = os.path.abspath(audio_file)
                    f.write(f"file '{abs_path}'\n")

            cmd = [
                "ffmpeg",
                "-loglevel",
                "error",
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

            subprocess.run(
                cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

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

    def convert_to_speech(self, text, output_path, voice="alloy", settings=None):
        """Alias for generate_speech with output_path parameter"""
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=settings.get("pitch", 1.0) if settings else 1.0,
            )

            response.stream_to_file(output_path)
            return output_path

        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")
