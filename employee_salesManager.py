import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery

from all_menu import *
from tags import *
from main import *
from insert_table import *
from  delete_table import *
from update_table import *

def employee_salesManager_callback_query(update, context):
    query = update.callback_query.data
    if query == "pasajes_gv":
        message = employee_salesManager_pasajes_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_PASAJE
    elif query == "prereserva_gv":
        message = employee_salesManager_prereserva_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_PRERESERVA
    else:
        return cancel(update, context)

def employee_salesManager_pasajes_callback_query(update, context):
    query = update.callback_query.data
    if query == "vender_pasaje":
        initialize_salesManager_prebooking(context)
        message = make_presell_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_SELLPASAJE
    elif query == "mod_pasaje":
        message = modif_pasaje_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_MODIFPASAJE
    elif query == "atras":
        message = for_user_type_start_menu("employee_salesManager", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER
    else:
        return cancel(update, context)

def employee_salesManager_prereserva_callback_query(update, context):
    query = update.callback_query.data
    if query == "prereserva_vigentes" or query == "pago_prereseva":
        message = employee_salesManager_prereserva_code_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_PRERESERVA_CODE
    elif query == "atras":
        message = for_user_type_start_menu("employee_salesManager", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER
    else:
        return cancel(update, context)

def employee_salesManager_prereserva_code(update, context):
    query = update.callback_query.data
    if query == "atras":
        message = employee_salesManager_prereserva_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_PRERESERVA
    elif query == "pagado":
        booking_is_paid_update(context.user_data["ID_Prereserva"]) 
        msg = "✅ Se ha pagado satisfactoriamente la prereserva ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_salesManager", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_SALESMANAGER        
    elif query == "eliminar":
        delete_booking(context.user_data["ID_Prereserva"])
        msg = "✅ Se ha eliminado satisfactoriamente la prereserva ✅"
        update.callback_query.message.delete()
        update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
        msg = for_user_type_start_menu("employee_salesManager", update.effective_user['first_name'])
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return EMPLOYEE_SALESMANAGER        
    else:
        return cancel(update, context)

def employee_salesmanager_modifpasaje_callback_query(update, context):
    query = update.callback_query.data.split("_")
    if query[0] == "atras":
        if query[1] == "1":
            message = employee_salesManager_pasajes_menu()
            update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
            return EMPLOYEE_SALESMANAGER_PASAJE
        elif query[1] == "2":
            message = modif_pasaje_menu()
            update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
            return EMPLOYEE_SALESMANAGER_MODIFPASAJE
        elif query[1] == "3":
            message = pasaje_futuro_menu()
            update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
            return EMPLOYEE_SALESMANAGER_MODIFPASAJE
    elif query[0] == "guardar":
        #AQUI CREOOO Q VA EL UPDATE DE LOS DATOS MODIFICADO
        pass
    else:
        return cancel(update, context)

def employee_salesManager_sellpasaje_data_callback_query(update, context):
    query = update.callback_query.data
    if query == "cant_pasajeros":
        update.callback_query.message.edit_text("Introduzca la cantidad de pasajes a reservar.")
        return EMPLOYEE_SALESMANAGER_CANT_PASAJEROS
    elif query == "guardar":
        if context.user_data['cant_pasajes'] == "" or context.user_data['origen'] == "" or context.user_data['destino'] == "" or context.user_data['aerolinea'] == "" or context.user_data['fecha'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_SALESMANAGER_SELLPASAJE
        msg = save_prebooking_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return SAVE_OWNER_PREBOOKING_SALESMANAGER
    elif query == "atras":
        message = employee_salesManager_pasajes_menu()
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_PASAJE
    else:
        return cancel(update, context)

def save_data_owner_booking(update, context):
    query = update.callback_query.data
    if query == "si":
        initialize_owner_prebooking_data(context)
        msg = into_data_owner_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_SALESMANAGER_INTO_DATA_OWNER
    elif query == "no" or query == "atras":
        message = make_prebooking_salesManager_refresh_menu(context)
        update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
        return EMPLOYEE_SALESMANAGER_SELLPASAJE
    else:
        return cancel(update, context)

def save_data_salesManager_callback_query(update, context):
    query = update.callback_query.data
    if query == "si":
        initialize_client_prebooking_data(context)
        context.user_data['index'] = 1
        msg = into_data_pasajero_client_menu(context)
        context.user_data['all_passeger'] = []
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_SALESMANAGER_INTO_DATA_PASS
    elif query == "no" or query == "atras":
        msg = into_data_owner_client_menu(context)
        msg[0] = data_owner_salesManager_refresh(msg[0], context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_SALESMANAGER_SELLPASAJE
    else:
        return cancel(update, context)

def into_data_passeger_salesManager_callback_query(update, context):
    query = update.callback_query.data
    if query == "nombre":
        update.callback_query.message.edit_text(f"Ingrese el nombre del pasajero {context.user_data['index']}")
        return NAME_PASSEGER_SALESMANAGER
    elif query == "apellidos":
        update.callback_query.message.edit_text(f"Ingrese el apellido del pasajero {context.user_data['index']}")
        return LAST_NAME_PASSEGER_SALESMANAGER
    elif query == "no_pasaporte":
        update.callback_query.message.edit_text(f"Ingrese el No de pasaporte del pasajero {context.user_data['index']}")
        return No_Passport_PASSEGER_SALESMANAGER
    elif query == "guardar":
        if context.user_data['passeger_name'] == "" or context.user_data['passeger_last_name'] == "" or context.user_data['passeger_country'] == "" or context.user_data['passeger_no_passport'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_SALESMANAGER_INTO_DATA_PASS
        msg = save_data_passenger_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_SALESMANAGER_PRERESERVA_DETAILS
    else:
        return cancel(update, context)

def into_data_owner_salesManager_callback_query(update, context):
    query = update.callback_query.data
    if query == "nombre":
        update.callback_query.message.edit_text(f"Ingrese el nombre del comprador.")
        return NAME_OWNER_SALESMANAGER
    elif query == "apellidos":
        update.callback_query.message.edit_text(f"Ingrese el apellido del comprador.")
        return LAST_NAME_OWNER_SALESMANAGER
    elif query == "no_pasaporte":
        update.callback_query.message.edit_text(f"Ingrese el No de pasaporte del comprador.")
        return No_Passport_OWNER_SALESMANAGER
    elif query == "guardar":
        if context.user_data['owner_name'] == "" or context.user_data['owner_last_name'] == "" or context.user_data['owner_country'] == "" or context.user_data['owner_no_passport'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return EMPLOYEE_SALESMANAGER_INTO_DATA_OWNER
        msg = save_data_owner_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return SAVE_PREBOOKING_SALESMANAGER
    else:
        return cancel(update, context)

def name_owner_salesManager_message_text(update, context):
    context.user_data['owner_name'] = update.message.text
    update.message.delete()
    msg = into_data_owner_client_menu(context)
    msg[0] = data_owner_salesManager_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_INTO_DATA_OWNER

def last_name_owner_salesManager_message_text(update, context):
    context.user_data['owner_last_name'] = update.message.text
    update.message.delete()
    msg = into_data_owner_client_menu(context)
    msg[0] = data_owner_salesManager_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_INTO_DATA_OWNER

def no_passport_owner_salesManager_message_text(update, context):
    no_passport = update.message.text
    update.message.delete()
    context.user_data['owner_no_passport'] = no_passport
    msg = into_data_owner_client_menu(context)
    msg[0] = data_owner_salesManager_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_INTO_DATA_OWNER

def name_passeger_salesManager_message_text(update, context):
    context.user_data['passeger_name'] = update.message.text
    update.message.delete()
    msg = into_data_pasajero_client_menu(context)
    msg[0] = data_passeger_salesManager_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_INTO_DATA_PASS

def last_name_passeger_salesManager_message_text(update, context):
    context.user_data['passeger_last_name'] = update.message.text
    update.message.delete()
    msg = into_data_pasajero_client_menu(context)
    msg[0] = data_passeger_salesManager_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_INTO_DATA_PASS

def no_passport_passeger_salesManager_message_text(update, context):
    no_passport = update.message.text
    update.message.delete()
    context.user_data['passeger_no_passport'] = no_passport
    msg = into_data_pasajero_client_menu(context)
    msg[0] = data_passeger_salesManager_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_INTO_DATA_PASS

def save_passeger_salesManager_callback_query(update, context): #REVISAR BIEN
    query = update.callback_query.data
    if query == "si":
        save_data(context)
        initialize_client_prebooking_data(context)
        context.user_data['index'] =  int(context.user_data['index']) + 1
        if context.user_data['index'] > context.user_data['cant_pasajes']:
            for item in context.user_data['all_passeger']:
                insert_client_booking(item)
     
            insert_client_booking([context.user_data["owner_name"], context.user_data["owner_last_name"], context.user_data["owner_country"], context.user_data["owner_no_passport"]])
            id_c = select_ID_client_using_no_passport(context.user_data["owner_no_passport"])[0][0]
            id_f = select_ID_Flight(context.user_data["origen"], context.user_data["destino"], context.user_data["aerolinea"], context.user_data["fecha"])[0][0]
            client_list = [item[3] for item in context.user_data['all_passeger']]

            insert_booking_datas(id_c, id_f, client_list)
            msg = "✅ Usted ha realizado satisfactoriamente la prereserva ✅"
            update.callback_query.message.delete()
            update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
            msg = for_user_type_start_menu("employee_salesManager", update.effective_user['first_name'])
            context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
            return EMPLOYEE_SALESMANAGER
        msg = into_data_pasajero_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return EMPLOYEE_SALESMANAGER_INTO_DATA_PASS
    elif query == "no" or query == "atras":
        pass
        #return new_client_callback_query(update, context)
    else:
        return cancel(update, context)

def save_data(context):
    context.user_data['all_passeger'].append([context.user_data['passeger_name'], context.user_data['passeger_last_name'], context.user_data['passeger_country'], context.user_data['passeger_no_passport']])

def employee_salesManager_cantPasajes_message_text(update, context):
    cant = update.message.text
    update.message.delete()
    if not cant.isdigit() or  int(cant) == 0:
        msg = "Introduzca la cantidad de pasajes a reservar. \n\n🚫Por favor introduzca solo la cantidad de pasajes a revervar🚫"
        try:
            update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        except:
            pass
        return EMPLOYEE_SALESMANAGER_CANT_PASAJEROS

    result = select_passengers_count(context, int(cant))
    
    if result != []: 
        context.user_data['cant_pasajes'] = int(cant)
    else:
        update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text="Introduzca la cantidad de pasajes a reservar. \n\n🚫No hay capacidad para la cantidad de pasajes introducidos.🚫", parse_mode = 'Markdown')

    msg = make_prebooking_salesManager_refresh_menu(context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return EMPLOYEE_SALESMANAGER_SELLPASAJE

def initialize_salesManager_prebooking(context):
    context.user_data["cant_pasajes"] = ""
    context.user_data["origen"] = ""
    context.user_data["destino"] = ""
    context.user_data["aerolinea"] = ""
    context.user_data["fecha"] = ""

def initialize_client_prebooking_data(context):
    context.user_data["passeger_name"] = ""
    context.user_data["passeger_last_name"] = ""
    context.user_data["passeger_country"] = ""
    context.user_data["passeger_no_passport"] = ""  

def initialize_owner_prebooking_data(context):
    context.user_data["owner_name"] = ""
    context.user_data["owner_last_name"] = ""
    context.user_data["owner_country"] = ""
    context.user_data["owner_no_passport"] = ""  

def data_passeger_salesManager_refresh(msg, context):
    if context.user_data['passeger_name'] != "":
        msg += f"\n Nombre: {context.user_data['passeger_name']}"

    if context.user_data['passeger_last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['passeger_last_name']}"

    if context.user_data['passeger_country'] != "":
        msg += f"\n Country: {context.user_data['passeger_country']}"
    
    if context.user_data['passeger_no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['passeger_no_passport']}"
    return msg

#PONER TODO EN LO Q DIGA PASSAGER OWNER
def data_owner_salesManager_refresh(msg, context):
    if context.user_data['owner_name'] != "":
        msg += f"\n Nombre: {context.user_data['owner_name']}"

    if context.user_data['owner_last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['owner_last_name']}"

    if context.user_data['owner_country'] != "":
        msg += f"\n Country: {context.user_data['owner_country']}"
    
    if context.user_data['owner_no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['owner_no_passport']}"
    return msg
    