import logging

import requests
from telegram import Bot
from telegram.ext import CommandHandler, Updater

# API key Dood.re
DOOD_RE_API_KEY = "your_dood_re_api_key"

# API token Telegram
TELEGRAM_API_TOKEN = "your_telegram_api_token"

# ID chat atau channel Telegram tempat video akan diupload
TELEGRAM_CHAT_ID = "your_telegram_chat_id"

# URL API Dood.re untuk mendapatkan link download video
DOOD_RE_VIDEO_URL = "https://dood.re/api/v1/video"

# Inisialisasi logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def download_video(video_id):
    """Mendownload video dari Dood.re menggunakan API."""
    # Kirim permintaan ke API Dood.re untuk mendapatkan link download video
    params = {"api_key": DOOD_RE_API_KEY, "video_id": video_id}
    response = requests.get(DOOD_RE_VIDEO_URL, params=params)

    # Cek apakah permintaan berhasil atau tidak
    if response.status_code == 200:
        # Ambil data video dari response
        video_data = response.content
        return video_data
    else:
        logger.error(f"Gagal mendapatkan video dari Dood.re: {response.text}")
        return None

def upload_video(video_data):
    """Mengupload video ke Telegram menggunakan API."""
    # Inisialisasi bot Telegram
    bot = Bot(token=TELEGRAM_API_TOKEN)

    # Kirim video ke channel atau chat yang ditentukan
    bot.send_video(chat_id=TELEGRAM_CHAT_ID, video=video_data)

def download_video_handler(update, context):
    """Fungsi yang dipanggil ketika pesan '/download' diterima oleh bot."""
    # Ambil video_id dari pesan yang dikirim pengguna
    video_id = update.message.text.split()[1]

    # Download video dari Dood.re
    video_data = download_video(video_id)

    # Cek apakah download berhasil atau tidak
    if video_data:
        # Upload video ke Telegram
        upload_video(video_data)
        update.message.reply_text("Video telah diupload!")
    else:
        update.message.reply_text("Gagal mendownload video dari Dood.re.")
