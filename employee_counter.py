import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User

from tags import *
from all_menu import *
from update_table import *
from main import *

#employee_counter

def employee_counter_callback_query(update, context):
    query = update.callback_query.data.split("_")
    if query[0] == "atras":
        if query[1] == "1":
            msg = for_user_type_start_menu("employee_counter", update.effective_user['first_name'])
            update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
            return EMPLOYEE_COUNTER
        elif query[1] == "2":
            msg = employee_counter_menu1(update.effective_user['first_name'])
            update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
            return EMPLOYEE_COUNTER
    elif query[0] == "cantMaletas":
        update.callback_query.message.edit_text(text="Introduzca la cantidad de maletas con que viaja el pasajero.", parse_mode = 'Markdown')
        return EMPLOYEE_COUNTER_MT
    elif query[0] == "check":
        if context.user_data["maletas"] == "":
            context.bot.answer_callback_query(context.user_data['id_query'], text="🚫Debe introducir primero la cantidad de maletas.🚫")
            return EMPLOYEE_COUNTER
        airfare_update(context.user_data["ID_C"], context.user_data["ID_F"], context.user_data["maletas"])
        msg = "✅Se ha chequado satisfactoriamente al pasajero✅"
        update.callback_query.message.edit_text(text=msg, parse_mode = 'Markdown')
        msg = employee_counter_menu2()
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_COUNTER
    else:
        return cancel(update, context)

def employee_counter_cantMaletas_message_text(update, context):
    maletas = update.message.text
    update.message.delete()
    if not maletas.isdigit():
        msg = "Introduzca la cantidad de maletas con que viaja el pasajero.\n\n🚫Por favor introduzca solo la cantidad de maletas con que viaja el pasajero.🚫"
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        return EMPLOYEE_COUNTER_MT

    context.user_data["maletas"] = maletas
    msg = employee_counter_menu3(context.user_data['info'])
    msg[0] += "\nCantidad de maletas: "+str(maletas)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_COUNTER




def initialize_employee_counter(context):
    context.user_data["vuelo"] = ""
    context.user_data["cliente"] = ""
    context.user_data["maletas"] = ""

