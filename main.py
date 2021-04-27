import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent, User
from random import getrandbits

TOKEN = '1663513841:AAHGbvXjXU6g69NlGRzV6KdlxGIMs_A_E28'

def start(update, context):
    # ANTES HAY REVISAR SI ESTA EN LA BD
    name = update.message.chat.first_name
    msg = f"Hola {name}, que desea hacer??"
    
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cliente", callback_data="new_client"))
    button_list.append(telegram.InlineKeyboardButton("Empleado", callback_data="new_employee"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.message.chat.send_message(text=msg, parse_mode = 'Markdown', reply_markup=reply_markup)


def build_menu(buttons, n_cols, header_buttons=None, header_buttons1=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]

    if header_buttons:
        menu.insert(0, header_buttons)
        menu.insert(1, header_buttons1)

    if footer_buttons:
        menu.append(footer_buttons)

    return menu


def main():
    update = Updater(TOKEN, use_context=True)
    dp = update.dispatcher
    dp.add_handler(CommandHandler('start', start))
    
    
    
    update.start_polling()
    update.idle()


if __name__ == '__main__':
    main()