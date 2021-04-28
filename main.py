import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User
from random import getrandbits

import os
import psycopg2

import create_table
import insert_table
import contains
import all_messages

from buttons import *
from tags import *


def start(update, context):
    user_type = contains.contains_user_start(update.message.chat.id)
    name = update.message.chat.first_name
    if user_type == "":
        msg = f"Hola {name}, que desea hacer??"
        button_list = []
        button_list.append(telegram.InlineKeyboardButton("Cliente", callback_data=NEW_CLIENT))
        button_list.append(telegram.InlineKeyboardButton("Empleado", callback_data=NEW_EMPLOYEE))
        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        update.message.chat.send_message(text=msg, parse_mode = 'Markdown', reply_markup=reply_markup)
    else:
        message = all_messages.message_menu(user_type, name)
        update.message.chat.send_message(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])

def new_client_callback_query(update, context):
    query = update.callback_query
    initialize_client(context)
    if query.data == NEW_CLIENT:
        button_list = []
        button_list.append(telegram.InlineKeyboardButton("Atras", callback_data=BACK))
        button_list.append(telegram.InlineKeyboardButton("Siguiente", callback_data=NEXT))
        button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data=CANCEL))
        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        update.callback_query.message.edit_text("Introduzca su Nombre.")
        return NAME_CLIENT

def initialize_client(context):
    context.user_data["name"] = ""
    context.user_data["apellidos"] = ""
    context.user_data["pais"] = ""

def name_client_callback_query(update, context):
    name = update.message.text
    context.user_data["name"] = name
    update.message.chat.send_message("Introduzca sus apellidos.")

def main():
    TOKEN = os.environ.get("TOKEN")
    update = Updater(TOKEN, use_context=True)
    dp = update.dispatcher
    dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(CommandHandler('a', test))
    
    new_client_callback = ConversationHandler(
        entry_points = [
            CallbackQueryHandler(new_client_callback_query, pass_user_data=True)
        ],
        states = {
			NAME_CLIENT:[MessageHandler(Filters.text, name_client_callback_query, pass_user_data=True)],
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