import os
import yt_dlp
from moviepy.editor import VideoFileClip
import whisper
import logging
import shutil

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Define constants for output directories
OUTPUT_DIR = "output"
VIDEO_OUTPUT_DIR = f"{OUTPUT_DIR}/video_file"
AUDIO_OUTPUT_DIR = f"{OUTPUT_DIR}/audio_file"
TEXT_OUTPUT_DIR = f"{OUTPUT_DIR}/text_file"


# Ensure all output directories exist
def create_output_directories():
    os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
    os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEXT_OUTPUT_DIR, exist_ok=True)


# Download YouTube video
def download_video_from_YT_link(url):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(VIDEO_OUTPUT_DIR, 'video_file.mp4'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
        logging.info(f"Download completed: {os.path.join(VIDEO_OUTPUT_DIR, 'video_file.mp4')}")
        return os.path.join(VIDEO_OUTPUT_DIR, 'video_file.mp4')

    except Exception as e:
        logging.error(f"Error during video download: {e}")
        return None


# Convert video to MP3
def convert_to_mp3(video_file):
    try:
        video = VideoFileClip(video_file)
        audio_file = os.path.join(AUDIO_OUTPUT_DIR, "audio_file.mp3")
        video.audio.write_audiofile(audio_file)
        logging.info(f"Audio conversion completed: {audio_file}")
        return audio_file

    except Exception as e:
        logging.error(f"Error during audio conversion: {e}")
        return None

    finally:
        video.close()


# Transcribe audio file
def transcribe_audio(audio_file):
    try:
        if not os.path.exists(audio_file):
            logging.error("Audio file does not exist.")
            return

        logging.info("Starting transcription...")
        model = whisper.load_model("base")
        transcribed_result = model.transcribe(audio_file)

        output_text_file = os.path.join(TEXT_OUTPUT_DIR, "transcribe.txt")
        with open(output_text_file, "w") as f:
            f.write(transcribed_result["text"])

        logging.info(f"Transcription completed and saved to: {output_text_file}")
        return output_text_file

    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return None


# Delete existing file
def delete_output_directory():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        logging.info(f"Deleted '{OUTPUT_DIR}' directory and all its contents.")
    else:
        logging.info(f"'{OUTPUT_DIR}' directory does not exist.")


# Main workflow
def main():
    input_url = input("Paste YouTube link: ")

    # Delete existing output folder
    delete_output_directory()

    # Create required directories
    create_output_directories()

    # Download video
    video_file = download_video_from_YT_link(input_url)

    if video_file:
        # Convert video to MP3
        audio_file = convert_to_mp3(video_file)

        if audio_file:
            # Transcribe audio
            transcribe_audio(audio_file)
        else:
            logging.error("Audio conversion failed. Transcription aborted.")
    else:
        logging.error("Video download failed. Aborting process.")


# Run the main function
if __name__ == "__main__":
    main()
