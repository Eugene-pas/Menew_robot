import localization
import numpy
import requests
from db import get_user_ingredients
from telegram import Update, constants
from telegram.ext import (
    ContextTypes,
    CommandHandler,
)


async def select_meal_with_your_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get all ingredients for user"""
    ingredients = get_user_ingredients(update.message.from_user.id)

    if ingredients is None or len(ingredients) == 0:
        await update.message.reply_text(
            localization.HAVE_NOT_INGREDIENTS,
            parse_mode=constants.ParseMode.MARKDOWN
        )
        return

    await update.message.reply_text(
        "Pleas, wait..."
    )

    recipes = []
    name_list = []

    for item in ingredients:
        list = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={item}").json()["meals"]
        if list != None and list.count != 0:
            recipes = numpy.concatenate((list, recipes))

    for item in recipes:
        name_list.append(item['strMeal'])

    unique, pos = numpy.unique(name_list, return_inverse=True)
    counts = numpy.bincount(pos)
    maxpos = counts.argmax()

    await update.message.reply_text(
        f"After analyzing your data, I found a dish that "
        f"contains *{counts[maxpos]}* of your ingredients. This is *{unique[maxpos]}*",
        parse_mode=constants.ParseMode.MARKDOWN
    )


select_meal_with_your_ingredients_handler = CommandHandler('select_meal_for_ingredients',
                                                           select_meal_with_your_ingredients)
