import os
import telebot
from dotenv import load_dotenv
import logging


load_dotenv()

# Configurar o logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
file_handler = logging.FileHandler("bot.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

# Suprimir logging excessivo da biblioteca httpx
logging.getLogger("httpx").setLevel(logging.WARNING)


API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

class TelegramBot:
    def __init__(self):
        logger.info("Inicializando o TelegramChatbot")
        self.default_message_reply = (
            "Olá! Gostaria de conversar com Nalim's BOT?"
        )
