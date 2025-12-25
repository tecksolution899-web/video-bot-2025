import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- ያንተ መረጃዎች በትክክል ገብተዋል ---
TOKEN = '7665281312:AAFl3Q71Fz_-A90jDRXHkCkjMTLugAnS3BA'
CHANNEL_ID = -1003426701331
CHANNEL_URL = 'https://t.me/fast_video_save_bot'
# ----------------------------------

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"የአባልነት ፍተሻ ስህተት: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "እንኳን ወደ Ethio Video Downloader ቦት በሰላም መጡ! 🚀\n\n"
        "ቪዲዮ ለማውረድ መጀመሪያ ቻናላችንን ይቀላቀሉ::"
    )
    await update.message.reply_text(welcome_msg)

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. መጀመሪያ አባል መሆኑን ይፈትሻል
    is_member = await check_membership(update, context)
    
    if not is_member:
        keyboard = [[InlineKeyboardButton("ቻናሉን ተቀላቀል ✅", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "⚠️ ቪዲዮ ለማውረድ መጀመሪያ ቻናላችንን መቀላቀል አለብዎት።\nከቀላቀሉ በኋላ ሊንኩን በድጋሚ ይላኩ።",
            reply_markup=reply_markup
        )
        return

    # 2. ሊንክ መሆኑን ማረጋገጥ
    url = update.message.text
    if "http" not in url:
        await update.message.reply_text("እባክዎ ትክክለኛ የቪዲዮ ሊንክ ይላኩ።")
        return

    status_msg = await update.message.reply_text("⏳ ቪዲዮው እየተወረደ ነው... እባክዎ ይጠብቁ።")
    user_id = update.effective_user.id
    file_name = f"{user_id}.mp4"
    
    try:
        # የyt-dlp ማስተካከያ (Indentation አስተካክያለሁ)
        ydl_opts = {
            'format': 'best',
            'outtmpl': file_name,
            'quiet': True,
            'no_warnings': True,
            'cookiefile': 'cookies.txt',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # 3. ቪዲዮውን መላክ
        with open(file_name, 'rb') as video:
            await update.message.reply_video(
                video=video,
                caption="ባለዎት ፍጥነት ተጠቅመው ስላወረዱ እናመሰግናለን! ✅\n\n@fast_video_save_bot"
            )
        
        # 4. ፋይሉን ማጥፋት
        await status_msg.delete()
        if os.path.exists(file_name):
            os.remove(file_name)
        
    except Exception as e:
        print(f"Download error: {e}")
        await update.message.reply_text(f"❌ ስህተት ተፈጥሯል! \nምክንያት፡ {str(e)}")
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("🚀 ቦቱ በሙሉ አቅሙ ስራ ጀምሯል!")
    app.run_polling()
import http.server
import socketserver
import threading

# Render ለሚጠይቀው Port ምላሽ ለመስጠት
def run_health_check():
    PORT = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

if __name__ == '__main__':
    # Health check በሌላ በኩል እንዲሰራ ማድረግ
    threading.Thread(target=run_health_check, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("🚀 ቦቱ በነፃው ሰርቨር ስራ ጀምሯል!")
    app.run_polling()



