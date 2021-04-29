import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User
from random import getrandbits

import os
import psycopg2

import create_table
import insert_table
import contains

from insert_table import *
from all_messages import *
from buttons import *
from tags import *

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

def start(update, context):
    user_type = contains.contains_user_start(update.message.chat.id)
    name = update.message.chat.first_name
    logger.info(f"El usuario {name}, ha iniciado el bot")
    if user_type == "":
        msg = f"Hola {name}, que desea hacer??"
        button_list = []
        button_list.append(telegram.InlineKeyboardButton("Cliente", callback_data=NEW_CLIENT))
        button_list.append(telegram.InlineKeyboardButton("Empleado", callback_data=NEW_EMPLOYEE))
        reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
        update.message.chat.send_message(text=msg, parse_mode = 'Markdown', reply_markup=reply_markup)
    else:
        message = message_menu(user_type, name)
        update.message.chat.send_message(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])

def new_client_callback_query(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']}, new_client")
    initialize_client(context)
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_start"))
    button_list.append(telegram.InlineKeyboardButton("Siguiente", callback_data="siguiente_lastName"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data=CANCEL))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.callback_query.message.edit_text(text="Introduzca su Nombre.", parse_mode = 'Markdown', reply_markup=reply_markup)
    return NAME_CLIENT

def last_name_client_callback_query(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']}, last_name_client")
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_name"))
    button_list.append(telegram.InlineKeyboardButton("Siguiente", callback_data="siguiente_country"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data=CANCEL))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.callback_query.message.edit_text(text="Introduzca sus Apellidos.", parse_mode = 'Markdown', reply_markup=reply_markup)
    return LAST_NAME_CLIENT

def country_client_callback_query(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']}, country_client")
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_lastName"))
    button_list.append(telegram.InlineKeyboardButton("Siguiente", callback_data="siguiente_end"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data=CANCEL))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.callback_query.message.edit_text(text="Introduzca su Pais.", parse_mode = 'Markdown', reply_markup=reply_markup)
    return COUNTRY_CLIENT

def initialize_client(context):
    context.user_data["name"] = ""
    context.user_data["last_name"] = ""
    context.user_data["country"] = ""

def name_client_message_text(update, context):
    name = update.message.text
    context.user_data["name"] = name
    logger.info(f"El usuario {update.effective_user['first_name']}, ha enviado el siguiente texto: name_client -> {name}")

def last_name_client_message_text(update, context):
    last_name = update.message.text
    context.user_data["last_name"] = last_name
    logger.info(f"El usuario {update.effective_user['first_name']}, ha enviado el siguiente texto: last_name_client -> {last_name}")
    

def country_client_message_text(update, context):
    country = update.message.text
    context.user_data["country"] = country
    logger.info(f"El usuario {update.effective_user['first_name']}, ha enviado el siguiente texto: country_client -> {country}")

def check_info_callback_query(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']}, check_info")
    name = context.user_data["name"]
    last_name = context.user_data["last_name"]
    country = context.user_data["country"]
    msg = f"Esta seguro que la informacion siguiente es correcta? \n\n\
        Nombre: {name}\n\
        Apellidos: {last_name}\n\
        Pais: {country}"
    button_list.append(telegram.InlineKeyboardButton("No", callback_data="atras_country"))
    button_list.append(telegram.InlineKeyboardButton("Si", callback_data="Done"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data=CANCEL))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    update.callback_query.message.edit_text(text=msg, parse_mode = 'Markdown', reply_markup=reply_markup)

def cancel_callback_query(update, context):
    logger.info(f"El usuario {update.effective_user['first_name']}, cancel")
    update.callback_query.message.delete()
    return ConversationHandler.END

def callback_query_start(update, context):
    query = update.callback_query.split('_')
    if query[0] == "atras":
        if query[1] == "start":
            return start(update, context)
        elif query[1] == "name":
            return new_client_callback_query(update, context)
        elif query[1] == "lastName":
            return last_name_client_callback_query(update, context)
        elif query[1] == "country":
            return country_client_callback_query(update, context)
    elif query[0] == "siguiente":
        if query[1] == "lastName":
            return last_name_client_callback_query(update, context)
        elif query[1] == "country":
            return country_client_callback_query(update, context)
        elif query[1] == "end":
            return check_info_callback_query(update, context)
    elif query[0] == "new":
        if query[1] == "client":
            return new_client_callback_query(update, context)
    elif query[0] == "Done":
        insert_cliente(context)
        message_menu("client", context.user_data["name"])
        return ConversationHandler.END
    elif query[0] == CANCEL:
        return cancel_callback_query(update, context)
    
        


def main():
    TOKEN = os.environ.get("TOKEN")
    update = Updater(TOKEN, use_context=True)
    dp = update.dispatcher
    #dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(CommandHandler('a', test))
    
    new_client_callback = ConversationHandler(
        entry_points = [
            CommandHandler('start', start)
        ],
        states = {
            #CLIENT: CallbackQueryHandler(new_client_callback_query, pass_user_data=True),
            CALLBACK_QUERY_START: [CallbackQueryHandler(callback_query_start)],
			NAME_CLIENT:[MessageHandler(Filters.text, name_client_message_text, pass_user_data=True)],
            LAST_NAME_CLIENT: [MessageHandler(Filters.text, last_name_client_message_text, pass_user_data=True)],
            COUNTRY_CLIENT: [MessageHandler(Filters.text, country_client_message_text, pass_user_data=True)],
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