import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *
from main import *
from insert_table import *

def employee_facilitiesSupervisior(update, context):
    query = update.callback_query.data
    if query == "añadir_instalacion":
        initialize_employee(context)
        msg = employee_facilitiesSupervisior_add_inst_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_FACILITIESSUPERVISOR_ADD
    elif query == "atras":
        msg = for_user_type_start_menu("employee_facilitiesSupervisor", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_FACILITIESSUPERVISOR
    else:
        return cancel(update, context)

def employee_facilitiesSupervisior_add_inst(update, context):
    query = update.callback_query.data
    if query == "name":
        msg = "Introduzca el nombre de la instalacion."
        update.callback_query.message.edit_text(text=msg, parse_mode = 'Markdown')
        return EMPLOYEE_FACILITIESSUPERVISOR_INST_NAME
    elif query == "guardar":
        if context.user_data['inst_name'] == "" or context.user_data['tipo_inst'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_FACILITIESSUPERVISOR_ADD
        insert_installation(select_ID_A_employee_using_id_telegram(update.effective_user['id'])[0], context.user_data['inst_name'],context.user_data['tipo_inst'])
        msg = "✅ Se ha añadido satisfactoriamente la instalacion ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_facilitiesSupervisor", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_FACILITIESSUPERVISOR
    elif query == "atras":
        msg = for_user_type_start_menu("employee_facilitiesSupervisor", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_FACILITIESSUPERVISOR
    else:
        return cancel(update, context)


def employee_facilitiesSupervisior_inst_name_message_text(update, context):
    name = update.message.text
    context.user_data['inst_name'] = name
    update.message.delete()
    msg = employee_facilitiesSupervisior_add_inst_menu()
    msg[0] = data_employee_fS_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_FACILITIESSUPERVISOR_ADD
    
def data_employee_fS_refresh(msg, context):
    if context.user_data['inst_name'] != "":
        msg += f"\nNombre de la instalcion: {context.user_data['inst_name']}"

    if context.user_data['tipo_inst'] != "":
        msg += f"\nTipo de Instalacion: {context.user_data['tipo_inst']}"

    return msg

def initialize_employee(context):
    context.user_data["inst_name"] = ""
    context.user_data["tipo_inst"] = ""
