import localization
import db
from telegram import Update, constants
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

ADD_INGREDIENTS = range(1)


async def start_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get all ingredients for user"""
    await update.message.reply_text(
        "In write your ingredients consecutively and through commas.\n"
        "*Example:\n*onion,tomato,apple\n\n"
        "_If you want to finish, type /done._",
        parse_mode=constants.ParseMode.MARKDOWN
    )

    return ADD_INGREDIENTS


async def add_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get all ingredients for user"""
    ingredients = update.message.text.split(',')

    if len(ingredients) == 0:
        await update.message.reply_text(
            localization.HAVE_NOT_INGREDIENTS /
            "\nRepyt /add_ingredients command",
            parse_mode=constants.ParseMode.MARKDOWN
        )

        return ConversationHandler.END

    db.add_ingredients(update.message.from_user.id, ingredients)

    await update.message.reply_text(
        "Ingredient added success.\n"
        "If you want to finish /done.\n"
        "You can see them /get_your_ingredient."
    )

    return ADD_INGREDIENTS


async def done_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get all ingredients for user"""
    await update.message.reply_text(
        "The add for ingredients is over.",
        parse_mode=constants.ParseMode.MARKDOWN
    )

    return ConversationHandler.END


add_ingredients_handler = ConversationHandler(
    entry_points=[CommandHandler("add_ingredients", start_add)],
    states={
        ADD_INGREDIENTS: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                           add_ingredients)
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("(^Done$|/done)"), done_add)]
)
