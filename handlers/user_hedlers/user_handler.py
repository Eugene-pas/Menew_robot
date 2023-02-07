import localization
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        localization.START_MAS
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=localization.UNKNOWN_MAS
    )


start_handler = CommandHandler('start', start)
unknown_handler = MessageHandler(filters.COMMAND, unknown)
