# telegram_bot.py

import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from utils import analyze_text, summarize_text, extract_text_from_file

DOWNLOAD_DIR = "downloads"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Use /help to see commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Available Commands:\n"
        "/start - Welcome message\n"
        "/help - Show help\n"
        "Send a text message to analyze it.\n"
        "Upload a PDF or DOCX file to get a summary."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("📈 Analyzing your message...")
    result = analyze_text(text)
    await update.message.reply_text(result)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file = await document.get_file()

    file_path = os.path.join(DOWNLOAD_DIR, document.file_name)
    await file.download_to_drive(file_path)
    await update.message.reply_text("📄 File received. Extracting text...")

    text = extract_text_from_file(file_path)
    if "Unsupported" in text:
        await update.message.reply_text("❌ Unsupported file type.")
    else:
        await update.message.reply_text("🧠 Summarizing the document...")
        summary = summarize_text(text)
        await update.message.reply_text(summary)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("❌ An error occurred. Please try again.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_error_handler(error_handler)

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
