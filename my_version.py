import os
import yt_dlp
from moviepy.editor import VideoFileClip
import whisper
import logging
import shutil

input_url = input("Paste youtube link: ")
output_folder = "output/video_file"
OUTPUT_DIR = "output"
os.makedirs(output_folder, exist_ok=True)


# used yt_dlp package to download the best quality video file
# passing url and output_path and in return getting best quality video file
def download_video_from_YT_link(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(output_path, 'video_file.mp4'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        logging.info(f"Download completed: {filename}")
        return os.path.join(output_path, 'video_file.mp4')
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None


# used moviepy package to convert downloaded video file to audio file
# here i'm passing video file and in return getting audio file in desired path
def convert_to_mp3(video_file):
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        output_folder = "output/audio_file"
        os.makedirs(output_folder, exist_ok=True)

        output_file = os.path.join(output_folder, "audio_file.mp3")
        audio.write_audiofile(output_file)
        logging.info(f"Audio conversion completed: {output_file}")
        return output_file
    except Exception as e:
        logging.error(f"An error occurred during conversion: {e}")
        return None
    finally:
        video.close()


# used open-ai's whisper package to convert audio file into txt file
def transcribe_audio():
    audio_file_path = "output/audio_file/audio_file.mp3"

    if not os.path.exists(audio_file_path):
        logging.error("Audio file does not exist.")
        return

    try:
        logging.info("Starting transcription...")

        model = whisper.load_model("base")
        logging.info("Whisper model loaded successfully.")

        transcribed_result = model.transcribe(audio_file_path)
        logging.info(f"Transcription result: {transcribed_result}")

        transcribe_output_folder = "output/text_file"
        os.makedirs(transcribe_output_folder, exist_ok=True)

        output_text_file = os.path.join(transcribe_output_folder, "transcribe.txt")
        with open(output_text_file, "w") as f:
            f.write(transcribed_result["text"])

        logging.info(f"Transcription completed and saved to: {output_text_file}")

    except Exception as e:
        logging.error(f"Error during transcription: {e}")


def delete_output_directory():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print(f"Deleted '{OUTPUT_DIR}' directory and all its contents.")
    else:
        print(f"'{OUTPUT_DIR}' directory does not exist.")


# first delete if any files are there.
# then download the video from youtube link
# then convert that video into audio_file
# then transcribe that audio_file

delete_output_directory()
downloaded_file = download_video_from_YT_link(input_url, output_folder)

if downloaded_file:
    audio_file = convert_to_mp3(downloaded_file)

    if audio_file:
        transcribe_audio()
    else:
        logging.error("Audio conversion failed. Transcription aborted.")
else:
    logging.error("Video download failed. Aborting process.")
