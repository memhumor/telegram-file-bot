import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = 8430312163
BOT_TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)

# Telegram Application
application = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("বট চালু আছে ✅ ফাইল পাঠাও")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("তুমি Admin না")
        return
    file = await update.message.document.get_file()
    await update.message.reply_text(f"ফাইল পাইছি: {update.message.document.file_name}")

# Handlers add
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.Document.ALL, handle_file))

@app_flask.route('/')
def home():
    return "Bot is running"

# Webhook setup for Render
@app_flask.route(f"/{BOT_TOKEN}", methods=["POST"])
async def webhook():
    await application.process_update(Update.de_json(request.get_json(force=True), application.bot))
    return "ok"

@app_flask.route("/setwebhook")
async def set_webhook():
    url = f"https://telegram-file-bot-kx57.onrender.com/{BOT_TOKEN}"
    await application.bot.set_webhook(url)
    return f"Webhook set to {url}"

if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
