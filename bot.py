import secret
import logging
from telegram.ext import ApplicationBuilder
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(secret.BOT_TOKEN).build()
