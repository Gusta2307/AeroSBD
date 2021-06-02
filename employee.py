import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User

from tags import *
from all_menu import *
from contains import *
from update_table import *

def new_employee_callback_query(update, context):
    message = new_employee_options()
    update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
    return NEW_EMPLOYEE_OPTIONS_CQ
    

def new_employee_verification_code_message_text(update, context):
    code = str(f"\'{update.message.text}\'")
    update.message.delete()
    result = isCodeCorrect(code)
    if result != []:
        id_telegram_employee_update(update.effective_user['id'], result[0][0])
        msg = for_user_type_start_menu(select_job(result[0][1]), update.effective_user['first_name'])
        print(msg)
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        cargo = result[0][1]
        if cargo == "Gerente de Ventas":
            return EMPLOYEE_SALESMANAGER
        elif cargo == "Empleado de Mostrador":
            return EMPLOYEE_COUNTER
        elif cargo == "Empleado de Migracion":
            return EMPLOYEE_IMMIGRATION
        elif cargo == "Empleado de Puerta de Salida":
            return EMPLOYEE_EXITDOOR
        elif cargo == "Operador de Vuelo":
            return EMPLOYEE_FLIGHTOPERATOR
        elif cargo == "Empleado de Recursos Humanos":
            return EMPLOYEE_HUMAN_RESOURCES
        elif cargo == "Jefe de Mecanica":
            return EMPLOYEE_CHIEFMACHANIC
        elif cargo == "Jefe de Almacen":
            return EMPLOYEE_WAREHOUSEMANGER
        elif cargo == "Jefe de Supervisor de Instalaciones":
            return EMPLOYEE_FACILITIESSUPERVISOR
        elif cargo == "Empleado de Instalacion":
            return EMPLOYEE_INSTALLATION
    else:
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text = "No existe este codigo de verificacion")
        message = new_employee_options()
        context.user_data['message_id'] = update.message.bot.send_message(chat_id=update.message.chat_id, text=message[0], parse_mode = 'Markdown', reply_markup=message[1]).message_id
        return NEW_EMPLOYEE_OPTIONS_CQ


def new_employee_options_callback_query(update, context):
    query = update.callback_query.data
    if query == "code":
        msg = new_employee_verification_code()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return NEW_EMPLOYEE
    elif query == "atras":
        msg = for_user_type_unknown_menu(update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return START
    else:
        return cancel(update, context)


def select_job(cargo):
    if cargo == "Gerente de Ventas":
        return "employee_salesManager" 
    elif cargo == "Empleado de Mostrador":
        return "employee_counter" 
    elif cargo == "Empleado de Migracion":
        return "employee_immigration"
    elif cargo == "Empleado de Puerta de Salida":
        return "employee_exitDoor"
    elif cargo == "Operador de Vuelo":
        return "employee_flightOperator"
    elif cargo == "Empleado de Recursos Humanos":
        return "employee_humanResources"
    elif cargo == "Jefe de Mecanica":
        return "employee_chiefMachanic"
    elif cargo == "Jefe de Almacen":
        return "employee_warehouseManager"
    elif cargo == "Jefe de Supervisor de Instalaciones":
        return "employee_facilitiesSupervisor"
    elif cargo == "Empleado de Instalacion":
        return "employee_installation"
    return cargo