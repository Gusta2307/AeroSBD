import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *

# employee_flightOperator

def employee_flightOperator_callback_query(update, context):
    query = update.callback_query.data
    if query =="programacion":
        msg = employee_flightOperator_prog()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_FLIGHTOPERATOR_PROG
    elif query == "atras":
        msg = for_user_type_start_menu("employee_flightOperator", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_FLIGHTOPERATOR
    else:
        return cancel(update, context)

def employee_flightOperator_prog_callback_query(update, context):
    query = update.callback_query.data
    if query == "atras":
        msg = for_user_type_start_menu("employee_flightOperator", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_FLIGHTOPERATOR
    else:
        return cancel(update, context)