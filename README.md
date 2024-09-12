# YouTube Video to Text Transcriber

This Python script downloads a YouTube video, converts its audio to MP3 format, and then transcribes the audio into text
using the Whisper speech recognition model.

## Features

- Downloads YouTube videos using `yt-dlp`.
- Converts video files to MP3 format using `moviepy`.
- Transcribes audio using the efficient `Whisper` model.
- Organizes output files into separate directories.
- Provides logging for easy debugging.
- You also need to install `ffmpeg` for the script to work.

## How to Use

1. **Clone the repository:**

  ```bash
  git clone https://github.com/skanimesh10/youtube-video-to-text.git
  cd youtube-video-to-text
  ```

2. **Install the required packages:**

 ```bash
 pip3 install -r requirements.txt
 ```

2. **Run the script:**

  ```bash
  python3 optimized_version.py
  ```

3. **Paste YouTube Link:**
   The script will prompt you to enter the YouTube video URL you want to transcribe.

  ```bash
  https://www.youtube.com/shorts/rjVTe_5HXow
  ```

## Output

Files will be saved in the following directory structure:

- **`output/video_file/video_file.mp4`**: The downloaded YouTube video.
- **`output/audio_file/audio_file.mp3`**: The audio extracted from the video.
- **`output/text_file/transcribe.txt`**: The transcribed text from the audio.

## Notes

- Ensure you have a stable internet connection for downloading videos.
- The transcription accuracy depends on the quality of the audio and the Whisper model used.
- You can change the output directory by modifying the `OUTPUT_DIR` constant in the script.

## Disclaimer

This project is for educational purposes only. Please respect YouTube's terms of service and copyright regulations.
