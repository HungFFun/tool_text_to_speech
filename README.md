# Text to Speech Converter

Ứng dụng chuyển đổi văn bản thành giọng nói sử dụng OpenAI TTS API với giao diện đồ họa.

## Tính năng

- Chuyển đổi văn bản thành giọng nói với nhiều giọng đọc khác nhau
- Hỗ trợ văn bản dài với xử lý đa luồng
- Trình phát audio với các chức năng:
  - Play/Pause
  - Stop
  - Tua tiến/lùi 10 giây
  - Thanh progress có thể kéo thả
- Hiển thị ước tính thời gian và chi phí
- Giao diện người dùng thân thiện

## Yêu cầu hệ thống

- Python 3.8 trở lên
- FFmpeg (cần thiết cho việc xử lý audio)
- OpenAI API key

## Cài đặt

1. Clone repository:

git clone https://github.com/yourusername/text-to-speech.git
cd text-to-speech

2. Cài đặt các dependencies:

pip install -r requirements.txt

3. Tạo file `.env` và thêm OpenAI API key:

OPENAI_API_KEY=your_openai_api_key

4. Cài đặt FFmpeg:

- Windows: Tải từ https://ffmpeg.org/download.html
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

5. Cấu hình OpenAI API key:

- Tạo file `.env` từ `.env.example`
- Thêm OpenAI API key của bạn vào file

## Sử dụng

1. Chạy ứng dụng:

python main.py

2. Sử dụng giao diện:

- Nhập văn bản vào ô text
- Chọn giọng đọc mong muốn
- Điều chỉnh các thông số (nếu cần)
- Nhấn "Convert" để bắt đầu chuyển đổi
- Sử dụng trình phát để nghe kết quả

## Cấu hình

- **Voice**: Chọn giọng đọc (alloy, echo, fable, onyx, nova, shimmer)
- **Pitch**: Điều chỉnh tốc độ đọc
- **Stability**: Độ ổn định của giọng đọc
- **Clarity**: Độ rõ ràng của giọng đọc

## Chi phí

- OpenAI tính phí $0.015 cho mỗi 1,000 ký tự
- Ứng dụng hiển thị ước tính chi phí trước khi chuyển đổi

## Xử lý lỗi thường gặp

1. **FFmpeg không được tìm thấy**

   - Đảm bảo FFmpeg đã được cài đặt và thêm vào PATH

2. **OpenAI API key không hợp lệ**

   - Kiểm tra file .env và API key

3. **Lỗi khi xử lý văn bản dài**
   - Văn bản sẽ tự động được chia thành các đoạn nhỏ hơn
   - Đảm bảo kết nối internet ổn định
