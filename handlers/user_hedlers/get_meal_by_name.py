import telegram.constants

import localization
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

FIND, GET_MEAL = range(2)

reply_keyboard = [
    ["Age", "Favourite colour"],
    ["Number of siblings", "Something else..."],
    ["Done"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


async def find_meal_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        "Pleas, write name of meal or /done."
    )

    return GET_MEAL


async def get_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_meal = update.message.text
    data_recipe = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={name_meal}").json()

    if data_recipe["meals"] == None:
        await update.message.reply_text(
            "Sorry, but I can not find this meal. :(\n"
            "If you wont continue writing somthing\n"
            "or not write /done."
        )
        return FIND

    receipt = f'[{data_recipe["meals"][0]["strMeal"]}]({data_recipe["meals"][0]["strMealThumb"]})\n' \
              f'_Category: {data_recipe["meals"][0]["strCategory"]}_\n' \
              f'_Area: {data_recipe["meals"][0]["strArea"]}_\n' \
              f'[Youtube video]({data_recipe["meals"][0]["strYoutube"]})\n' \
              f'*Instructions:* {data_recipe["meals"][0]["strInstructions"]}\n' \
              f'*Ingredients:*\n'

    for num in range(20):
        ingredient = data_recipe["meals"][0][f"strIngredient{num + 1}"]
        measure = data_recipe["meals"][0][f"strMeasure{num + 1}"]

        if ingredient != None and  ingredient != "" and  measure != None and  measure != "":
            receipt = receipt + f'{data_recipe["meals"][0][f"strIngredient{num + 1}"]} - ' \
                                f'{data_recipe["meals"][0][f"strMeasure{num + 1}"]}\n'

    await update.message.reply_text(receipt, parse_mode=telegram.constants.ParseMode.MARKDOWN)
    return FIND


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Finding meal of done.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


find_meal_by_name_handler = ConversationHandler(
    entry_points=[CommandHandler("find_meal_by_name", find_meal_by_name)],
    states={
        FIND: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, find_meal_by_name
            )
        ],
        GET_MEAL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_recipe)
        ]
    },
    fallbacks=[CommandHandler("done", done)]
)
