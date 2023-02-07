import localization
from db import get_user_ingredients
from telegram import Update, constants
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)


async def get_your_ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get all ingredients for user"""
    ingredients = get_user_ingredients(update.message.from_user.id)

    if ingredients.count == 0:
        await update.message.reply_text(
            localization.HAVE_NOT_INGREDIENTS,
            parse_mode=constants.ParseMode.MARKDOWN
        )

    str_list = "*Your ingredients:*\n"
    for item in ingredients:
        str_list = str_list + item + "\n"

    await update.message.reply_text(
        str_list,
        parse_mode=constants.ParseMode.MARKDOWN
    )


get_your_ingredient_handler = CommandHandler('get_your_ingredient', get_your_ingredient)
