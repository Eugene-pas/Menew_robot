from bot import application
from handlers.user_hedlers.user_handler import start_handler, help_handler
from handlers.user_hedlers.get_meal_by_name import find_meal_by_name_handler

if __name__ == '__main__':
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(find_meal_by_name_handler)
    application.run_polling()
