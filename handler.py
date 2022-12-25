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
