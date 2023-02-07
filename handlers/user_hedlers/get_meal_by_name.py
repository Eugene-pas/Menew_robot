import telegram.constants
import localization
import requests
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

GET_MEAL, GET_INFO = range(2)

reply_keyboard = [
    ["Recipe", "Ingredients"],
    ["Done"]
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

recipe_id = None


async def find_meal_by_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the conversation and ask user for input."""
    await update.message.reply_text(
        localization.FIND_MEAL_HELP
    )

    return GET_MEAL


async def get_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_meal = update.message.text
    data_recipe = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={name_meal}").json()

    if data_recipe["meals"] == None:
        await update.message.reply_text(
            "Sorry, but I can not find this meal. :(\n"
            "If you wont continue writing the name of the meal\n"
            "or not write /done."
        )
        return GET_MEAL

    context.user_data["recipe_id"] = data_recipe["meals"][0]["idMeal"]

    receipt = f'[{data_recipe["meals"][0]["strMeal"]}]({data_recipe["meals"][0]["strMealThumb"]})\n' \
              f'_Category: {data_recipe["meals"][0]["strCategory"]}_\n' \
              f'_Area: {data_recipe["meals"][0]["strArea"]}_\n' \
              f'[Youtube video]({data_recipe["meals"][0]["strYoutube"]})\n'

    await update.message.reply_text(
        receipt,
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_markup=markup
    )
    return GET_INFO


async def get_recipe_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data["recipe_id"]
    if user_data == None:
        update.message.reply_text("I don't know which recipe to show you.")
        return GET_MEAL

    data_recipe = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={user_data}").json()

    if data_recipe["meals"] == None:
        await update.message.reply_text(
            "Sorry, but I can not find this meal. :(\n"
            "If you wont continue writing somthing\n"
            "or not write Done."
        )
        return GET_MEAL

    receipt = f'*{data_recipe["meals"][0]["strMeal"]}*\n' \
              f'*Instructions:*\n{data_recipe["meals"][0]["strInstructions"]}\n'

    await update.message.reply_text(
        receipt,
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        localization.FIND_MEAL_HELP
    )

    return GET_MEAL


async def get_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data["recipe_id"]

    if user_data == None:
        update.message.reply_text("I don't know which recipe to show you.")
        return GET_MEAL

    data_recipe = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={user_data}").json()

    if data_recipe["meals"] == None:
        await update.message.reply_text(
            "Sorry, but I can not find this meal. :(\n"
            "If you wont continue writing somthing\n"
            "or not write /done."
        )
        return GET_MEAL

    receipt = f'*{data_recipe["meals"][0]["strMeal"]}*\n' \
              f'*Ingredients:*\n'

    for num in range(20):
        ingredient = data_recipe["meals"][0][f"strIngredient{num + 1}"]
        measure = data_recipe["meals"][0][f"strMeasure{num + 1}"]

        if ingredient != None and ingredient != "" and measure != None and measure != "":
            receipt = receipt + f'{data_recipe["meals"][0][f"strIngredient{num + 1}"]} - ' \
                                f'{data_recipe["meals"][0][f"strMeasure{num + 1}"]}\n'

    await update.message.reply_text(
        receipt,
        parse_mode=telegram.constants.ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        localization.FIND_MEAL_HELP
    )
    return GET_MEAL


def update_recipe_id(user_data):
    if "recipe_id" in user_data:
        del user_data["recipe_id"]


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "The search for dishes is over.",
        reply_markup=ReplyKeyboardRemove()
    )

    user_data = context.user_data
    update_recipe_id(user_data)

    user_data.clear()
    return ConversationHandler.END


find_meal_by_name_handler = ConversationHandler(
    entry_points=[CommandHandler("find_meal_by_name", find_meal_by_name)],
    states={
        GET_MEAL: [
            MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("(^Done$|^Recipe$|^Ingredients$)")),
                           get_recipe)
        ],
        GET_INFO: [
            MessageHandler(filters.Regex("^Recipe$")
                           & ~(filters.COMMAND | filters.Regex("^Done$")),
                           get_recipe_text),
            MessageHandler(filters.Regex("^Ingredients$")
                           & ~(filters.COMMAND | filters.Regex("^Done$")),
                           get_ingredients)
        ]

    },
    fallbacks=[MessageHandler(filters.Regex("(^Done$|/done)"), done)]
)
