import subprocess
import os

class AudioMerger:
    def __init__(self):
        self.audio_files = []
    
    def add_audio(self, audio_path):
        self.audio_files.append(audio_path)
    
    def merge_audio_files(self, output_path):
        if not self.audio_files:
            return False
            
        # Create file list
        with open('file_list.txt', 'w') as f:
            for audio_file in self.audio_files:
                f.write(f"file '{audio_file}'\n")
        
        # Merge using ffmpeg
        try:
            subprocess.run([
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', 'file_list.txt',
                '-c', 'copy',
                output_path
            ], check=True)
            
            # Clean up
            os.remove('file_list.txt')
            return True
            
        except subprocess.CalledProcessError:
            if os.path.exists('file_list.txt'):
                os.remove('file_list.txt')
            return False 