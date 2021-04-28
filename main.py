import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User
from random import getrandbits

import os
import psycopg2

import create_table
import insert_table
import contains
import buttons
import all_messages

from tags import *


def start(update, context):
    user_type = contains.contains_user_start(update.message.chat.id)
    name = update.message.chat.first_name
    if user_type == "":
        msg = f"Hola {name}, que desea hacer??"
        create_table.create_tables()
        button_list = []
        button_list.append(telegram.InlineKeyboardButton("Cliente", callback_data=NEW_CLIENT))
        button_list.append(telegram.InlineKeyboardButton("Empleado", callback_data=NEW_EMPLOYEE))
        reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=2))
        update.message.chat.send_message(text=msg, parse_mode = 'Markdown', reply_markup=reply_markup)
    else:
        message = all_messages.message_menu(user_type, name)
        update.message.chat.send_message(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])

def new_client_callback_query(update, context):
    query = update.callback_query
    if query.data == NEW_CLIENT:
        print("yeap")

def main():
    TOKEN = os.environ.get("TOKEN")
    update = Updater(TOKEN, use_context=True)
    dp = update.dispatcher
    dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(CommandHandler('a', test))
    
    new_client_callback = ConversationHandler(
        entry_points = [
            CallbackQueryHandler(new_client_callback_query)
        ],
        states = {
			#PREMIOS:[CallbackQueryHandler(premios_callbackQuery, pass_user_data=True)],
		}, 
        fallbacks = []
    )

    dp.add_handler(new_client_callback)
    #SE CREAN LAS TABLAS DE LA BD
    create_table.create_tables()
    
    
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    update.start_webhook(listen = "0.0.0.0", port = PORT, url_path = TOKEN)
    update.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")

	
	
	


if __name__ == '__main__':
    main()