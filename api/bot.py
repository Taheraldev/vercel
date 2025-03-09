from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from http import HTTPStatus
from fastapi import FastAPI, Request, Response

app = FastAPI()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# تهيئة البوت
telegram_app = Application.builder().token(BOT_TOKEN).build()

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت يعمل على Vercel 🚀")

# رد على أي رسالة
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"لقد أرسلت: {update.message.text}")

# تسجيل ال handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.post("/api/bot")
async def webhook(request: Request):
    update_data = await request.json()
    update = Update.de_json(update_data, telegram_app.bot)
    await telegram_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)
