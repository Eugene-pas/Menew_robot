from bot import application
from user_handler import start_handler, unknown_handler

if __name__ == '__main__':
    application.add_handler(start_handler)
    application.add_handler(unknown_handler)
    application.run_polling()
