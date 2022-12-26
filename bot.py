# main.py

import logging
import os
import re
import aria2p
import requests

from telegram import Bot
from telegram.ext import CommandHandler, Updater

# Import the .env file
from dotenv import load_dotenv
load_dotenv()

# Get the API keys and session IDs from the environment variables
DOOD_RE_API_KEY = os.getenv("DOOD_RE_API_KEY")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Inisialisasi logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the allowed IDs from the environment variable
allowed_ids_string = os.getenv("ALLOWED_IDS")
allowed_ids = [int(id) for id in allowed_ids_string.split(",")]

# URL API Dood.re untuk mendapatkan link download video
DOOD_RE_VIDEO_URL = "https://dood.re/api/v1/video"

# Regex untuk mengecek apakah video_id terdiri dari kombinasi angka dan huruf
video_id_regex = r"^[a-zA-Z0-9]+$"

# Inisialisasi logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi aria2p
aria2 = aria2p.API()

def download_video(video_id):
    """Mendownload video dari Dood.re menggunakan aria2p."""
    # Validasi apakah video_id terdiri dari kombinasi angka dan huruf
    if not re.match(video_id_regex, video_id):
        return None

    # Kirim permintaan ke API Dood.re
    params = {
        "api_key": DOOD_RE_API_KEY,
        "video_id": video_id
    }
    try:
        response = requests.get(DOOD_RE_VIDEO_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"RequestException: {e}")
        return None

    # Ambil link download video dari hasil respon API
    data = response.json()
    download_url = data.get("url")
    if not download_url:
        logger.error(f"API response: {data}")
        return None

    # Download video menggunakan aria2p
    file_name = f"{video_id}.mp4"
    aria2.add_uris([download_url], options={"out": file_name})
    download = aria2.get_download(download_url)
    download.wait_until_complete()

    # Baca file video yang telah didownload
    try:
        with open(file_name, "rb") as f:
            video_data = f.read()
    except IOError as e:
        logger.error(f"IOError: {e}")
        return None

    # Hapus file video setelah selesai digunakan
    os.remove(file_name)

    return video_data
    
def upload_video(video_data, update):
    """Mengupload video ke Telegram menggunakan API."""
    # Inisialisasi bot Telegram
    bot = Bot(token=TELEGRAM_API_TOKEN)

    # Kirim video ke channel atau chat yang ditentukan
    try:
        bot.send_video(chat_id=TELEGRAM_CHAT_ID, video=video_data)
    except Exception as e:
        update.message.reply_text("Gagal mengirim video. Error: {}".format(e))

def download_video_handler(update, context):
    """Fungsi yang dipanggil ketika pesan '/download' diterima oleh bot."""
    # Ambil video_id dari pesan yang dikirim pengguna
    video_id = update.message.text.split()
    if len(video_id) < 2:
        update.message.reply_text("Video ID tidak ditemukan.")
        logger.error("Video ID not found")
        return
    video_id = video_id[1]

    # Validasi apakah video_id terdiri dari kombinasi angka dan huruf
    if not re.match(video_id_regex, video_id):
        update.message.reply_text("Video ID harus terdiri dari angka dan huruf.")
        logger.error("Invalid video ID")
        return

    # Get the user ID of the sender
    user_id = update.effective_user.id

    # Check if the user ID is in the list of allowed IDs
    if user_id not in allowed_ids:
        update.message.reply_text("You are not authorized to use this command.")
        logger.error("Unauthorized user ID")
        return

    # Kirim pesan pemberitahuan ke pengguna bahwa proses download dimulai
    update.message.reply_text("Mendownload video dari Dood.re...")
    logger.info("Downloading video from Dood.re")

    # Download video dari Dood.re
    video_data = download_video(video_id)
    if not video_data:
        update.message.reply_text("Gagal mendownload video.")
        logger.error("Failed to download video")
        return

    # Kirim pesan pemberitahuan ke pengguna bahwa proses upload dimulai
    update.message.reply_text("Mengupload video ke Telegram...")
    logger.info("Uploading video to Telegram")

    # Upload video ke Telegram
    upload_video(video_data, update)
    update.message.reply_text("Video berhasil diupload.")
    logger.info("Video successfully uploaded")

def main():
    # Inisialisasi bot Telegram
    updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Tambahkan handler untuk pesan '/download'
    download_handler = CommandHandler("download", download_video_handler)
    dispatcher.add_handler(download_handler)

    # Jalankan bot
    updater.start_polling()
    updater.idle()
if __name__ == "__main__":
    main()