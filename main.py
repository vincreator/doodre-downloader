# main.py

import logging
import os
import re
import aria2p

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
    # Validasi apakah video_id merupakan kombinasi angka dan huruf
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
        return None

    # Ambil link download video dari hasil respon API
    data = response.json()
    download_url = data.get("url")
    if not download_url:
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
        update.message.reply_text

def download_video_handler(update, context):
    """Fungsi yang dipanggil ketika pesan '/download' diterima oleh bot."""
    # Ambil video_id dari pesan yang dikirim pengguna
    video_id = update.message.text.split()[1]

    # Validasi apakah video_id merupakan string angka
    if not video_id.isdigit():
        update.message.reply_text("Video ID harus berupa angka.")
        return

    # Kirim pesan pemberitahuan ke pengguna bahwa proses download dimulai
    update.message.reply_text("Mendownload video dari Dood.re...")

    # Download video dari Dood.re
    video_data = download_video(video_id)

    # Cek apakah download berhasil atau tidak
    if video_data:
        # Kirim pesan pemberitahuan ke pengguna bahwa proses download selesai
        update.message.reply_text("Mendownload video dari Dood.re selesai!")

        # Kirim pesan pemberitahuan ke pengguna bahwa proses upload dimulai
        update.message

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
