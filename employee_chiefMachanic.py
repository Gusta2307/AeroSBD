import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *
from insert_table import *
from main import *

# employee_chiefMachanic

def employee_chiefMachanic_callback_query(update, context):
    query = update.callback_query.data
    if query == "añadir_nave":
        msg = employee_chiefMachanic_add_nave_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_CHIEFMACHANIC_ADD_NAVE
    elif query == "atras_1":
        msg = for_user_type_start_menu("employee_chiefMachanic", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_CHIEFMACHANIC
    elif query == "add_repair":
        initialize_repair(context)
        msg = employee_chiefMachanic_add_repair_refresh_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_CHIEFMACHANIC_ADD_REPAIR
    else:
        return cancel(update, context)

def employee_chiefMachanic_add_repair_callback_query(update, context):
    query = update.callback_query.data
    if query == "duracion":
        update.callback_query.message.edit_text("Ingrese la cantidad de dias de la reparacion")
        return EMPLOYEE_CHIEFMACHANIC_DURACION
    elif query == "guardar":
        if context.user_data['repair'] == [] or context.user_data['days'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_CHIEFMACHANIC
        print("OK", context.user_data['days'])
        insert_apply_repair_repair(Enrollment=context.user_data['enrollment'], Cod_R=context.user_data['repair'][0], Days=context.user_data['days'], ID_AeroP=select_ID_A_employee_using_id_telegram(update.effective_user['id'])[0], ID_I=select_id_installation_employee(update.effective_user['id'])[0])
        msg = "✅ Usted ha añadido satisfactoriamente una nueva reparacion ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_chiefMachanic", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_CHIEFMACHANIC
    elif query == "atras_2":
        repair = select_airplane_repairs(context.user_data['enrollment'], select_ID_A_employee_using_id_telegram(update.effective_user['id'])[0], select_id_installation_employee(update.effective_user['id'])[0])
        msg=employee_chiefMachanic_refresh_menu(repair[0][0], repair[1])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_CHIEFMACHANIC
    else:
        return cancel(update, context)

def employee_chiefMachanic_duracion_message_text(update, context):
    dias = update.message.text
    update.message.delete()
    if not dias.isdigit() or int(dias) <= 0:
        msg = "Ingrese la cantidad de dias de la reparacion. \n\n🚫Por favor introduzca solo la cantidad de dias🚫"
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        return EMPLOYEE_CHIEFMACHANIC_DURACION
    context.user_data['days'] = dias
    msg = employee_chiefMachanic_add_repair_refresh_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_CHIEFMACHANIC_ADD_REPAIR

def employee_chiefMachanic_add_nave_callback_query(update, context):
    query = update.callback_query.data
    if query == "matricula":
        update.callback_query.message.edit_text("Ingrese la matricula")
        return EMPLOYEE_CHIEFMACHANIC_MATRICULA
    elif query == "capacidad":
        update.callback_query.message.edit_text("Ingrese la capacidad")
        return EMPLOYEE_CHIEFMACHANIC_CAPACITY
    elif query == "tipo":
        update.callback_query.message.edit_text("Ingrese la clasificacion.")
        return EMPLOYEE_CHIEFMACHANIC_TIPO
    elif query == "guardar":
        if context.user_data['matricula'] == [] or context.user_data['capacidad'] == "" or context.user_data['tipo'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_CHIEFMACHANIC_ADD_NAVE
        insert_airplane(context.user_data["matricula"], context.user_data["tipo"], context.user_data["capacidad"])
        msg = "✅ Usted ha añadido satisfactoriamente una nueva nave ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_chiefMachanic", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_CHIEFMACHANIC
    elif query == "atras":
        msg = for_user_type_start_menu("employee_chiefMachanic", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_CHIEFMACHANIC
    return cancel(update, context)

def employee_chiefMachanic_matricula_message_text(update, context):
    context.user_data['matricula'] = update.message.text
    update.message.delete()
    msg = employee_chiefMachanic_add_nave_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_CHIEFMACHANIC_ADD_NAVE

def employee_chiefMachanic_capacidad_message_text(update, context):
    capacidad = update.message.text
    update.message.delete()
    if not capacidad.isdigit() or int(capacidad) == 0:
        msg = "Introduzca la capacidad de la nave. \n\n🚫Por favor introduzca solo la capacidad de la nave🚫"
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        return EMPLOYEE_CHIEFMACHANIC_CAPACITY
    context.user_data['capacidad'] = capacidad
    msg = employee_chiefMachanic_add_nave_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_CHIEFMACHANIC_ADD_NAVE

def employee_chiefMachanic_tipo_message_text(update, context):
    context.user_data['tipo'] = update.message.text
    update.message.delete()
    msg = employee_chiefMachanic_add_nave_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_CHIEFMACHANIC_ADD_NAVE


def initialize_nave(context):
    context.user_data["matricula"] = ""
    context.user_data["capacidad"] = ""
    context.user_data["tipo"] = ""

def initialize_repair(context):
    context.user_data["repair"] = []
    context.user_data["days"] = ""
