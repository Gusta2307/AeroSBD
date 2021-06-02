import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *
from insert_table import *

#employee_warehouseManager

def employee_warehouseManager_callback_query(update, context):
    query = update.callback_query.data
    if query == "añadir_producto":
        initialize_employee(context)
        msg = employee_warehouseManager_add_prod_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_WAREHOUSEMANGER_ADD_PROD
    elif query == "atras":
        msg = for_user_type_start_menu("employee_warehouseManager", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_WAREHOUSEMANGER
    else:
        return cancel(update, context)

def employee_warehouseManager_addProd_callback_query(update, context):
    query = update.callback_query.data
    if query == "name_prod":
        update.callback_query.message.edit_text(text="Introduzca el nombre del producto.", parse_mode = 'Markdown')
        return EMPLOYEE_WAREHOUSEMANGER_NAME_PROD
    elif query == "cant":
        update.callback_query.message.edit_text(text="Introduzca la cantidad del producto a añadir.", parse_mode = 'Markdown')
        return EMPLOYEE_WAREHOUSEMANGER_CANT
    elif query == "precio":
        update.callback_query.message.edit_text(text="Introduzca el precio del producto a añadir.", parse_mode = 'Markdown')
        return EMPLOYEE_WAREHOUSEMANGER_PRICE
    elif query == "guardar": 
        if context.user_data['nameProd'] == "" or context.user_data['cant'] == "" or context.user_data['price'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_WAREHOUSEMANGER_ADD_PROD
        insert_product(context.user_data["nameProd"], context.user_data["cant"], context.user_data["price"], select_ID_A_employee_using_id_telegram(update.effective_user['id']), select_id_installation_employee(update.effective_user['id']))
        msg = "✅ Se ha añadido satisfactoriamente un nuevo producto ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_warehouseManager", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_WAREHOUSEMANGER
    elif query == "atras":
        msg = for_user_type_start_menu("employee_warehouseManager", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_WAREHOUSEMANGER
    else:
        return cancel(update, context)

def employee_warehouseManager_nameProd_message_text(update, context):
    nameProd = update.message.text
    context.user_data['nameProd'] = nameProd
    update.message.delete()
    msg = employee_warehouseManager_add_prod_menu()
    msg[0] = data_employee_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_WAREHOUSEMANGER_ADD_PROD

def employee_warehouseManager_cant_message_text(update, context):
    cant = update.message.text
    update.message.delete()
    if not cant.isdigit() or  int(cant) == 0:
        msg = "Introduzca la cantidad.\n\n🚫Por favor introduzca solo la cantidad del producto a verificar🚫"
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        return EMPLOYEE_WAREHOUSEMANGER_CANT
    context.user_data['cant'] = cant
    msg = employee_warehouseManager_add_prod_menu()
    msg[0] = data_employee_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_WAREHOUSEMANGER_ADD_PROD

def employee_warehouseManager_price_message_text(update, context):
    price = update.message.text
    context.user_data['price'] = price
    update.message.delete()
    msg = employee_warehouseManager_add_prod_menu()
    msg[0] = data_employee_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_WAREHOUSEMANGER_ADD_PROD

def initialize_employee(context):
    context.user_data["nameProd"] = ""
    context.user_data["cant"] = ""
    context.user_data["price"] = ""

def data_employee_refresh(msg, context):
    if context.user_data['nameProd'] != "":
        msg += f"\nNombre: {context.user_data['nameProd']}"

    if context.user_data['cant'] != "":
        msg += f"\nCantidad: {context.user_data['cant']}"

    if context.user_data['price'] != "":
        msg += f"\nPrecio: {context.user_data['price']}"
    
    return msg   
