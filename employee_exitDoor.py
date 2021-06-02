import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *

#employee_exitDoor

def employee_exitDoor_callback_query(update, context):
    query = update.callback_query.data
    if query == "list_compl":
        pass_list = select_all_passengers_in_flight(context.user_data["id_vuelo"])
        print(pass_list)
        msg = employee_warehouseManager_completeList_menu(make_msg(pass_list))
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_EXITDOOR_COMPL_LIST
    elif query == "atras":
        msg = for_user_type_start_menu("employee_exitDoor", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_EXITDOOR
    return cancel(update, context)

def employee_exitDoor_complete_List_callback_query(update, context):
    query = update.callback_query.data
    if query == "atras":
        msg = employee_exitDoor_passenger_list_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_EXITDOOR
    else:
        return cancel(update, context)

def employee_exitDoor_client_to_client_callback_query(update, context):
    pass


def make_msg(list_passenger):
    msg = ""
    index = 1
    for item in list_passenger:
        msg +=str(index)+". "+item[3]+" "+item[0]+" "+item[1]+" "+item[2]+'\n'
        index +=1
    return msg
