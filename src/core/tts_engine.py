from openai import OpenAI
import os
import time
import subprocess
from queue import Queue
from threading import Thread


class TTSEngine:
    def __init__(self):
        self.output_dir = os.path.abspath("output")
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
            output_file = os.path.join(
                self.output_dir, f"speech_{int(time.time()*1000)}.mp3"
            )

            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text,
                speed=settings.get("pitch", 1.0) if settings else 1.0,
            )

            response.stream_to_file(output_file)
            return output_file

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

    def generate_speech_parallel(self, text, voice="alloy", settings=None):
        """Xử lý song song với dynamic workers"""
        # Tối ưu kích thước chunks
        chunks = self.optimize_chunk_size(text)
        total_chunks = len(chunks)
        audio_files = [None] * total_chunks
        errors = []

        # Tạo và khởi động workers
        num_workers = min(self.max_workers, total_chunks)
        workers = []
        for _ in range(num_workers):
            t = Thread(target=self.worker)
            t.start()
            workers.append(t)

        # Đưa tasks vào queue
        for i, chunk in enumerate(chunks):
            self.task_queue.put((i, chunk, voice, settings))

        # Thêm None vào queue để signal workers dừng lại
        for _ in range(num_workers):
            self.task_queue.put(None)

        # Xử lý kết quả khi có
        completed = 0
        while completed < total_chunks:
            result = self.result_queue.get()
            if len(result) == 2:  # Successful result
                chunk_index, audio_file = result
                audio_files[chunk_index] = audio_file
            else:  # Error occurred
                chunk_index, _, error = result
                errors.append(f"Chunk {chunk_index}: {error}")

            completed += 1
            if self.progress_callback:
                self.progress_callback(completed, total_chunks)

        # Đợi tất cả workers hoàn thành
        for worker in workers:
            worker.join()

        # Kiểm tra lỗi
        if errors:
            raise Exception("\n".join(errors))

        # Lọc bỏ các None values (nếu có)
        valid_files = [f for f in audio_files if f is not None]

        if not valid_files:
            raise Exception("No audio files were generated successfully")

        return valid_files

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
