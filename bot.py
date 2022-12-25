import logging
import os
import subprocess

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

def run_aria2(download_url, file_name):
    """Menjalankan perintah aria2 untuk mendownload file."""
    subprocess.run(["aria2c", download_url, "--out", file_name])

def download_video(video_id):
    """Mendownload video dari Dood.re menggunakan aria2."""
    # Kirim permintaan ke API Dood.re untuk mendapatkan link download video
    params = {"api_key": DOOD_RE_API_KEY, "video_id": video_id}
    response = requests.get(DOOD_RE_VIDEO_URL, params=params)

    # Cek apakah permintaan berhasil atau tidak
    if response.status_code == 200:
        # Ambil link download dari data response
        download_url = response.json()["url"]

        # Buat nama file hasil download dengan menambahkan ekstensi .mp4
        file_name = f"{video_id}.mp4"

        # Download file menggunakan aria2
        run_aria2(download_url, file_name)

        # Cek apakah file hasil download sudah ada
        if os.path.exists(file_name

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

    # Validasi apakah video_id merupakan string angka
    if not video_id.isdigit():
        update.message.reply_text("Video ID harus berupa angka.")
        return

    # Download video dari Dood.re
    video_data = download_video(video_id)

    # Cek apakah download berhasil atau tidak
    if video_data:
        # Upload video ke Telegram
        upload_video(video_data)
        update.message.reply_text("Video telah diupload!")
    else:
        update.message.reply_text("Gagal mendownload video dari Dood.re.")

def main():
    # Inisialisasi updater
    updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Tambahkan handler untuk pesan '/download'
    download_handler = CommandHandler('download', download_video_handler)
    dispatcher.add_handler(download_handler)

    # Mulai polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()