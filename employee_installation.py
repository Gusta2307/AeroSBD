import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *
from insert_table import *
from buttons import *

#employee_installation

def employee_installation_callback_query(update, context):
    query = update.callback_query.data
    if query == "compra":
        initialize_employee(context)
        msg = employee_installation_purchases_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_INSTALLATION_PURCHASES
    elif query == "almacen":
        initialize_employee(context)
        msg = employee_installation_wareHouse_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_INSTALLATION_WAREHOUSE
    else:
        return cancel(update, context)

def employee_installation_purchases_callback_query(update, context):
    query = update.callback_query.data
    if query == "cant":
        update.callback_query.message.edit_text(text="Introduzca la cantidad.", parse_mode = 'Markdown')
        return EMPLOYEE_INSTALLATION_PURCHASES_CANT
    elif query == "guardar":
        if context.user_data['codigo_prod'] == "" or context.user_data['cant_prod'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_INSTALLATION_PURCHASES
        insert_buy(context.user_data["codigo_prod"], context.user_data["cant_prod"], select_id_installation_employee(update.effective_user['id']), select_ID_A_employee_using_id_telegram(update.effective_user['id']))
        msg = "✅ Usted ha realizado satisfactoriamente la compra ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_installation", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_INSTALLATION
    elif query == "atras":
        msg = for_user_type_start_menu("employee_installation",update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_INSTALLATION
    else:
        return cancel(update, context)

def employee_installation_warehouse_callback_query(update, context):
    query = update.callback_query.data
    if query == "atras":
        msg = for_user_type_start_menu("employee_installation",update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_INSTALLATION
    elif query == "atras_1":
        msg = employee_installation_wareHouse_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_INSTALLATION_WAREHOUSE
    else:
        return cancel(update, context)


def initialize_employee(context):
    context.user_data["codigo_prod"] = ""
    context.user_data["cant_prod"] = ""
    context.user_data["producto"] = ""  

def employee_installation_purchases_code_prod_message_text(update, context):
    code_product = update.message.text
    update.message.delete()
    context.user_data["codigo_prod"] = code_product
    msg = employee_installation_purchases_refresh_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_INSTALLATION_PURCHASES

def employee_installation_purchases_cant_message_text(update, context):
    cant = update.message.text
    update.message.delete()
    if not cant.isdigit() or  int(cant) == 0:
        msg = "Introduzca la cantidad.\n\n🚫Por favor introduzca solo la cantidad del producto a comprar🚫"
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        return EMPLOYEE_INSTALLATION_PURCHASES_CANT
    context.user_data["cant_prod"] = cant
    msg = employee_installation_purchases_refresh_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_INSTALLATION_PURCHASES