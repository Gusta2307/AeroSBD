import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def build_menu(buttons, n_cols, header_buttons=None, header_buttons1=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)
        menu.insert(1, header_buttons1)

    if footer_buttons:
        menu.append(footer_buttons)

    return menu

def cancel(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']}, cancel")
    update.callback_query.message.delete()
    return ConversationHandler.END
    