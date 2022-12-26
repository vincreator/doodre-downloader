# handler.py

def download_video_handler(update, context):
    """Fungsi yang dipanggil ketika pesan '/download' diterima oleh bot."""
    # Ambil video_id dari pesan yang dikirim pengguna
    video_id = update.message.text.split()[1]

    # Kirim pesan pemberitahuan ke pengguna bahwa proses download dimulai
    update.message.reply_text("Mendownload video dari Dood.re...")

    # Download video dari Dood.re
    video_data = download_video(video_id)

    # Cek apakah download berhasil atau tidak
    if video_data:
        # Kirim pesan pemberitahuan ke pengguna bahwa proses download selesai
        update.message.reply_text("Mendownload video dari Dood.re selesai!")

        # Kirim pesan pemberitahuan ke pengguna bahwa proses upload dimulai
        update.message.reply_text("Mengupload video ke Telegram...")

        # Upload video ke Telegram
        upload_video(video_data, update)

        # Kirim pesan pemberitahuan ke pengguna bahwa proses upload selesai
        update.message.reply_text("Mengupload video ke Telegram selesai!")
    else:
        # Kirim pesan pemberitahuan ke pengguna bahwa terjadi kesalahan saat download
        update.message.reply_text("Terjadi kesalahan saat mendownload video dari Dood.re.")