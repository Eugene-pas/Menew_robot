import localization
import db
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and offer help to users. When new user invite this fun add his in db"""
    db.create_user(
        update.message.from_user.id,
        update.message.from_user.username
    )
    await update.message.reply_text(
        localization.START_MAS
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show list commands."""
    await update.message.reply_text(
        "/find_meal_by_name - search for meal by name\n"
        "/get_your_ingredient - get all your ingredients\n"
        "/select_meal_for_ingredients - get meal according to the ingredients"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=localization.UNKNOWN_MAS
    )


start_handler = CommandHandler('start', start)
unknown_handler = MessageHandler(filters.COMMAND, unknown)
help_handler = CommandHandler('help', help)
