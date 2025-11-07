from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp
import os

TOKEN = os.environ.get("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("👋 أهلاً! اكتب اسم أي أغنية وأنا هجيبها لك ✅")

def download_music(update, context):
    query = update.message.text
    update.message.reply_text(f"🎧 جاري البحث عن: {query}")

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": "%(title)s.%(ext)s"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)
        file_name = ydl.prepare_filename(info['entries'][0])
        mp3_file = file_name.rsplit('.', 1)[0] + ".mp3"

    update.message.reply_audio(audio=open(mp3_file, 'rb'))
    os.remove(mp3_file)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_music))

updater.start_polling()
