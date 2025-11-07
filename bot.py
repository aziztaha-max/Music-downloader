import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8410121628:AAGS4966KWFYH6q2m2TM5ty2L9ZJgHwVrec"

# تحميل صوت من يوتيوب بالرابط
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ اكتب لينك بعد الأمر /link")
        return
    
    url = context.args[0]
    await update.message.reply_text("⏳ جاري التحميل ...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.mp3",
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_audio(audio="song.mp3")
        os.remove("song.mp3")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

# بحث وتنزيل من الاسم
async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ اكتب اسم الأغنية بعد /song")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 جاري البحث عن:\n{query}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "song.mp3",
        "quiet": True,
        "default_search": "ytsearch",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])

        await update.message.reply_audio(audio="song.mp3")
        os.remove("song.mp3")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 أهلا بيك!\n\n"
        "استخدم:\n"
        "/song اسم الأغنية 🎶\n"
        "/link رابط اليوتيوب 🔗\n\n"
        "وهجيبلك الأغنية MP3 ✅"
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", song))
    app.add_handler(CommandHandler("link", link))
    print("✅ Bot Running...")
    app.run_polling()
