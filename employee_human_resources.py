import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from string import ascii_letters, ascii_uppercase, digits
import random
from all_menu import *
from tags import *
from insert_table import *
from delete_table import *
from main import *

def employee_human_resources_options_callback_query(update, context):
    query = update.callback_query.data
    if query == "empleados":
        message = employee_list_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_LIST
    elif query == "añadir_empleados":
        message = employee_add_menu()
        initialize_employee(context)
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_ADD
    else:
        return cancel(update, context)

def employee_list_callback_query(update, context):
    query = update.callback_query.data
    if query == "atras": 
        message = for_user_type_start_menu("employee_humanResources", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_HUMAN_RESOURCES
    elif query == "eliminar" or query == "atras_1":
        if query == "eliminar":
            delete_employee(context.user_data['del_employee'][2])
            context.bot.answer_callback_query(update.callback_query.id, text="✅Se ha eliminado satisfactoriamente al empleado✅")
        message = employee_list_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_LIST
    else:
        return cancel(update, context)

def employee_add_callback_query(update, context):
    query = update.callback_query.data
    if query == "carnet":
        context.user_data['id_query'] = update.callback_query.id 
        update.callback_query.message.edit_text(text="Introduzca el numero de Carnet del nuevo empleado.", parse_mode = 'Markdown')
        return EMPLOYEE_DNI    
    elif query == "nombre":
        update.callback_query.message.edit_text(text="Introduzca el nombre del nuevo empleado.", parse_mode = 'Markdown')
        return EMPLOYEE_NAME
    elif query == "apellidos":
        update.callback_query.message.edit_text(text="Introduzca el apellido del nuevo empleado.", parse_mode = 'Markdown')
        return EMPLOYEE_LAST_NAME    
    elif query == "atras":
        msg = for_user_type_start_menu("employee_humanResources", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_HUMAN_RESOURCES
    elif query == "guardar":
        return save_new_employee(update, context)
    else:
        return cancel(update, context)

def dni_employee_message_text(update, context):
    dni = update.message.text
    update.message.delete()
    if not dni.isdigit():
        context.bot.answer_callback_query(context.user_data['id_query'], text="🚫El carnet de identidad debe ser digitos🚫")
        return
    context.user_data["dni_employee"] = dni
    msg = employee_add_menu()
    msg[0] = data_employee_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_ADD

def name_employee_message_text(update, context):
    name = update.message.text
    context.user_data['name_employee'] = name
    update.message.delete()
    msg = employee_add_menu()
    msg[0] = data_employee_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_ADD

def data_employee_refresh(msg, context):
    if context.user_data['name_employee'] != "":
        msg += f"\nNombre: {context.user_data['name_employee']}"

    if context.user_data['last_name_employee'] != "":
        msg += f"\nApellidos: {context.user_data['last_name_employee']}"

    if context.user_data['dni_employee'] != "":
        msg += f"\nCarnet: {context.user_data['dni_employee']}"

    if context.user_data['country'] != "":
        msg += f"\nCountry: {context.user_data['country']}"
    
    if context.user_data['job'] != "":
        msg += f"\nCargo: {context.user_data['job']}"
    
    return msg    

def last_name_employee_message_text(update, context):
    name = update.message.text
    context.user_data['last_name_employee'] = name
    update.message.delete()
    msg = employee_add_menu()
    msg[0] = data_employee_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_ADD

def initialize_employee(context):
    context.user_data["name_employee"] = ""
    context.user_data["last_name_employee"] = ""
    context.user_data["country"] = ""
    context.user_data["dni_employee"] = ""
    context.user_data["job"] = ""
    context.user_data["verif_code"] = ""
    context.user_data["ID_I"] = ""

def pwd():
    caracteres = ascii_letters + ascii_uppercase + digits
    cadena_aleatoria = ''.join(random.choice(caracteres) for caracter in range(8))
    return str(cadena_aleatoria)

def save_new_employee(update, context):
    if context.user_data["name_employee"] != "" and context.user_data["last_name_employee"] != "" \
        and context.user_data["country"] != "" and context.user_data["dni_employee"] != "" and context.user_data["job"] != "":
        context.user_data["verif_code"] = pwd()
        insert_employee(update, context)
    
        msg = "✅Se ha añadido satisfactoriamente el nuevo empleado✅ \n\n"
        msg += "Codigo de Verificacion: ```{0}```".format(context.user_data["verif_code"])
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_humanResources", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_HUMAN_RESOURCES
    else:
        context.bot.answer_callback_query(update.callback_query.id, text="🚫Debe rellenar todos los campos.🚫")
        return EMPLOYEE_ADD


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
