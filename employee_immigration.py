import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *
from select_from_table import *
from update_table import *
from insert_table import *

def employee_immigration_options_callback_query(update, context):
    query = update.callback_query.data
    msg = ""
    if query == "aceptar":
        if context.user_data["type_c"] == "ce":
            passengers_on_update(context.user_data["ID_C"], context.user_data["ID_F"], 1)
            msg = "✅Aprobada la entrada al pais✅"
        else:
            insert_passenger_in_Passenger_Flow(context.user_data["ID_C"], context.user_data["ID_F"], 1)
            msg = "✅Aprobada la salida del pais✅"

        update.callback_query.message.delete()
        context.bot.answer_callback_query(update.callback_query.id, text=msg)
        msg = for_user_type_start_menu("employee_immigration", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_IMMIGRATION
    elif query == "denegar":
        if context.user_data["type_c"] == "ce":
            passengers_on_update(context.user_data["ID_C"], context.user_data["ID_F"], 0)
            msg = "🚫Denegada la entrada al pais🚫"
        else:
            insert_passenger_in_Passenger_Flow(context.user_data["ID_C"], context.user_data["ID_F"], 0)
            msg = "🚫Denegada la salida del pais🚫"
                    
        update.callback_query.message.delete()
        context.bot.answer_callback_query(update.callback_query.id, text=msg)
        msg = for_user_type_start_menu("employee_immigration", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_IMMIGRATION
        
        return EMPLOYEE_IMMIGRATION
    elif query == "atras":
        msg = for_user_type_start_menu("employee_immigration", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_IMMIGRATION
    else:
        return cancel(update, context)
