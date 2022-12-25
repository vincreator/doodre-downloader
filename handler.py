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
