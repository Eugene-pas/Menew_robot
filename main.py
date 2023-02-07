from bot import application
from handlers.user_hedlers.user_handler import start_handler, help_handler
from handlers.user_hedlers.get_meal_by_name import find_meal_by_name_handler
from handlers.user_hedlers.get_user_ingredient import get_your_ingredient_handler
from handlers.user_hedlers.selection_of_meal import select_meal_with_your_ingredients_handler
from handlers.user_hedlers.add_ingredients import add_ingredients_handler

if __name__ == '__main__':
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(find_meal_by_name_handler)
    application.add_handler(get_your_ingredient_handler)
    application.add_handler(select_meal_with_your_ingredients_handler)
    application.add_handler(add_ingredients_handler)
    application.run_polling()
