import os
import logging
from dotenv import load_dotenv
from app.groq_call import groc_config

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    filters,
)

# Carregar variáveis de ambiente
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

class TelegramBot:
    def __init__(self):
        logger.info("Inicializando o TelegramChatbot")
        self.default_message_reply = "Olá! Gostaria de conversar com Nalim's BOT?"
        self.TELEGRAM_TOKEN = API_KEY

    def start_message(self):
        logger.info("Menu loaded...")
        try:
            menu = self.default_message_reply
            return menu
        
        except Exception as e:
            logger.error(f"Erro ao carregar o menu: {e}")
            raise
            
    def generate_keyboard(self, menu, prefix_menu="submenu_", prefix_action="action_"):
        logger.info("Gerando teclado inline")
        keyboard = [
            [InlineKeyboardButton("Sim", callback_data=f"{prefix_action}1")],
            [InlineKeyboardButton("Não", callback_data=f"{prefix_action}2")],
        ]
        logger.info("Teclado inline gerado com sucesso")
        return keyboard
    
    async def button(self, update: Update, context: CallbackContext):
        query = update.callback_query
        await query.answer()

        # Condicional baseado na escolha do usuário
        if query.data == "action_1":
            response_text = "Ok! Faça sua pergunta:"
        elif query.data == "action_2":
            response_text = "OK! Quando precisar de mim, estarei a disposição!"
        else:
            response_text = "Opção desconhecida."
        
        logger.info('Opção selecionada pelo usuário')
        # Edita a mensagem original com a resposta
        await query.edit_message_text(text=response_text)
    async def start(self, update: Update, context: CallbackContext):
        logger.info("Comando /start recebido")
        menu = self.start_message()
        keyboard = self.generate_keyboard(menu)
        await update.message.reply_text(
            text=menu, reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        

    def start_bot(self):
        try:
            logger.info("Inicializando a aplicação do bot")
            application = (
                ApplicationBuilder()
                .token(self.TELEGRAM_TOKEN)
                .pool_timeout(20)
                .connect_timeout(15)
                .read_timeout(60)  # Aumentar o tempo de leitura
                .write_timeout(60)  # Aumentar o tempo de escrita
                .build()
            )
            
            # Adicionar os handlers
            start_handler = CommandHandler("start", self.start)
            application.add_handler(start_handler)
            
            # Handler para lidar com as respostas do teclado inline
            button_handler = CallbackQueryHandler(self.button)
            application.add_handler(button_handler)
            
            # Iniciar o bot
            application.run_polling()
            
        except Exception as e:
            logger.error(f"Erro ao iniciar o bot: {e}")
            raise