import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, User
import os
import psycopg2
from datetime import *  

from create_table import *
from contains import *
from select_from_table import *
from insert_table import *
from all_menu import *
from buttons import *
from tags import *
from main import *

def new_client_callback_query(update, context):
    initialize_client(context)
    message = client_registration_menu(update.effective_user['first_name'])
    update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
    return CLIENT_REGISTRATION

def client_registration_callback_query(update, context):
    query = update.callback_query.data
    if query == "nombre":
        update.callback_query.message.edit_text("Ingrese su nombre")
        return NAME_CLIENT
    elif query == "apellidos":
        update.callback_query.message.edit_text("Ingrese sus apellidos")
        return LAST_NAME_CLIENT
    elif query == "no_pasaporte":
        context.user_data['id_query'] = update.callback_query.id
        update.callback_query.message.edit_text("Ingrese su numero de pasaporte")
        return No_Passport_CLIENT
    elif query == "atras":
        return start(update, context, True)
    elif query == "guardar":
        if context.user_data['name'] == "" or context.user_data['last_name'] == "" or context.user_data['country'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return CLIENT_REGISTRATION
        msg = save_data_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return SAVE_DATA_CLIENT
    else:
        return cancel(update, context)

def name_client_callback_query(update, context):
    context.user_data['name'] = update.message.text
    update.message.delete()
    msg = client_registration_menu(update.effective_user['first_name'])
    msg[0] = data_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_REGISTRATION

def last_name_client_callback_query(update, context):
    context.user_data['last_name'] = update.message.text
    update.message.delete()
    msg = client_registration_menu(update.effective_user['first_name'])
    msg[0] = data_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_REGISTRATION

def country_client_callback_query(update, context):
    context.user_data['country'] = update.message.text
    update.message.delete()
    msg = client_registration_menu(update.effective_user['first_name'])
    msg[0] = data_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_REGISTRATION

def no_passport_client_callback_query(update, context):
    no_passport = update.message.text
    update.message.delete()
    context.user_data['no_passport'] = no_passport
    msg = client_registration_menu(update.effective_user['first_name'])
    msg[0] = data_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_REGISTRATION

def initialize_client(context):
    context.user_data["name"] = ""
    context.user_data["last_name"] = ""
    context.user_data["country"] = ""
    context.user_data["no_passport"] = ""

def data_client_refresh(msg, context):
    if context.user_data['name'] != "":
        msg += f"\n Nombre: {context.user_data['name']}"

    if context.user_data['last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['last_name']}"

    if context.user_data['country'] != "":
        msg += f"\n Country: {context.user_data['country']}"
    
    if context.user_data['no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['no_passport']}"
    
    return msg

def data_passeger_client_refresh(msg, context):
    if context.user_data['passeger_name'] != "":
        msg += f"\n Nombre: {context.user_data['passeger_name']}"

    if context.user_data['passeger_last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['passeger_last_name']}"

    if context.user_data['passeger_country'] != "":
        msg += f"\n Country: {context.user_data['passeger_country']}"
    
    if context.user_data['passeger_no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['passeger_no_passport']}"
    
    return msg

def save_data_client_callback_query(update, context):
    query = update.callback_query.data
    if query == "si":
        insert_client(update, context)
        msg = for_user_type_start_menu("client", update.effective_user['first_name'])
        update.callback_query.message.delete()
        context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        return CLIENT_OPTIONS
    elif query == "no" or query == "atras":
        msg = client_registration_menu(update.effective_user['first_name'])
        msg[0] = data_client_refresh(msg[0], context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_REGISTRATION
    else:
        return cancel(update, context)

def client_options_callback_query(update, context):
    query = update.callback_query.data
    if query == "prereserva_client": 
        msg = prebooking_client_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_PREBOOKING
    elif query == "vuelos_fut_client":
        result = select_client_future_flight(update.effective_user['id'])
        count = 1
        msg = ""
        if result != None and result != []:
            for row in result:
                msg += "\n Codigo de Vuelo: " + str(row[0])
                msg += "\n Aerolinea: " + str(row[1])
                msg += "\n Aeropuerto de Salida: " + str(row[2])
                msg += "\n F/H de Salida: " + modif_date(str(row[3]))
                msg += "\n Aeropuerto de Llegada: " + str(row[4])
                msg += "\n F/H de Llegada: " + modif_date(str(row[5]))
                msg += "\n Precio por pasaje: " + str(row[6])
                msg += "\n ---------------------------------------------------------"

                if count % 5 == 0:
                    update.callback_query.message.chat.send_message(text = msg)
                    msg =""

                count += 1
            
            if msg != "":
                update.callback_query.message.chat.send_message(text = msg)
        else:
            context.bot.answer_callback_query(update.callback_query.id, text="🚫No tienes vuelos futuros existentes🚫")
    else:
        return cancel(update, context)

def modif_date(dateHour):
    date_hour = dateHour.split(' ')
    hour = date_hour[1].split(':')
    result = date_hour[0] + " " + hour[0] + ":" + hour[1]
    return str(result)

def client_prebooking_callback_query(update, context):
    query = update.callback_query.data
    if query == "ver_prereservas":
        result = select_client_booking(update.effective_user['id'])
        count = 1
        msg= ""
        if result != None and result != []:
            update.callback_query.message.delete()
            for row in result:
                msg += "\n ID_Prereserva: " + str(row[0])
                msg += "\n F/H Prereserva: " + modif_date(str(row[1]))
                msg += "\n Codigo de vuelo: " + str(row[2])
                msg += "\n Aerolinea: " + str(row[3])
                msg += "\n Cantidad de pasajes: " + str(row[4])
                msg += "\n Aeropuerto de Salida: " + str(row[5])
                msg += "\n F/H de Salida: " + modif_date(str(row[7]))
                msg += "\n Aeropuerto de Llegada: " + str(row[6])
                msg += "\n F/H de Llegada: " + modif_date(str(row[8]))
                msg += "\n Precio por pasaje: " + str(row[9])
                msg += "\n ---------------------------------------------------------"

                if count % 5 == 0:
                    update.callback_query.message.chat.send_message(text = msg)
                    msg =""

                count += 1
            
            if msg != "":
                update.callback_query.message.chat.send_message(text = msg)
            
            msg = prebooking_client_menu()
            context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
        else:
            context.bot.answer_callback_query(update.callback_query.id, text="🚫No tienes prereservas existentes🚫")
    elif query == "realizar_prereserva":
        initialize_client_prebooking(context)
        msg = make_prebooking_client_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_MAKE_PREBOOKING
    elif query == "atras":
        msg = for_user_type_start_menu("client", update.effective_user['first_name'])
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_OPTIONS
    else:
        return cancel(update, context)

def client_make_prebooking_callback_query(update, context):
    query = update.callback_query.data
    if query == "cant_pasajeros":
        context.user_data['id_query'] = update.callback_query.id
        update.callback_query.message.edit_text("Introduzca la cantidad de pasajes a reservar.")
        return CLIENT_CANT_PASAJES
    elif query == "guardar":
        if context.user_data['cant_pasajes'] == "" or context.user_data['origen'] == "" or context.user_data['destino'] == "" or context.user_data['aerolinea'] == "" or context.user_data['fecha'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return CLIENT_MAKE_PREBOOKING
        msg = save_prebooking_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return SAVE_PREBOOKING_CLIENT
    elif query == "atras":
        msg = prebooking_client_menu()
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_PREBOOKING
    else:
        return cancel(update, context)

def save_prebooking_client_callback_query(update, context):
    query = update.callback_query.data
    if query == "si":
        initialize_client_prebooking_data(context)
        context.user_data['index'] = 1
        msg = into_data_pasajero_client_menu(context)
        context.user_data['all_passeger'] = []
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_INTO_DATA_PASS
    elif query == "no" or query == "atras":
        msg = make_prebooking_client_menu()
        msg[0] = data_client_prebooking_refresh(msg[0], context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_MAKE_PREBOOKING
    else:
        return cancel(update, context)

def prebooking_data_passenger_client_callback_query(update, context):
    query = update.callback_query.data
    if query == "nombre":
        update.callback_query.message.edit_text(f"Ingrese el nombre del pasajero {context.user_data['index']}")
        return NAME_PASSEGER
    elif query == "apellidos":
        update.callback_query.message.edit_text(f"Ingrese el apellido del pasajero {context.user_data['index']}")
        return LAST_NAME_PASSEGER
    elif query == "no_pasaporte":
        update.callback_query.message.edit_text(f"Ingrese el No de pasaporte del pasajero {context.user_data['index']}")
        return No_Passport_PASSEGER
    elif query == "guardar":
        if context.user_data['passeger_name'] == "" or context.user_data['passeger_last_name'] == "" or context.user_data['passeger_country'] == "" or context.user_data['passeger_no_passport'] == "":
            context.bot.answer_callback_query(update.callback_query.id, text="🚫Todos los campos deben ser completados🚫")
            return CLIENT_INTO_DATA_PASS
        msg = save_data_passenger_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_SAVE_DATA_PASS
    else:
        return cancel(update, context)

def save_passeger_client_callback_query(update, context):
    query = update.callback_query.data
    if query == "si":
        save_data(context)
        initialize_client_prebooking_data(context)
        context.user_data['index'] = int(context.user_data['index']) + 1
        if context.user_data['index'] > context.user_data['cant_pasajes']:
            for item in context.user_data['all_passeger']:
                insert_client_booking(item)
            #context.user_data['all_passeger'].append(None,None,None,select_ID_client_using_id_telegram(update.effective_user['id'])[0][0])
            id_c = select_ID_client_using_id_telegram(update.effective_user['id'])[0][0]
            id_f = select_ID_Flight(context.user_data["origen"], context.user_data["destino"], context.user_data["aerolinea"], context.user_data["fecha"])[0][0]
            client_list = [item[3] for item in context.user_data['all_passeger']]

            insert_booking_datas(id_c, id_f, client_list)
            msg = "✅ Usted ha realizado satisfactoriamente la prereserva ✅"
            update.callback_query.message.delete()
            update.callback_query.message.chat.send_message(text=msg, parse_mode = 'Markdown')
            msg = for_user_type_start_menu("client", update.effective_user['first_name'])
            context.user_data['message_id'] = update.callback_query.message.chat.send_message(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1]).message_id
            return CLIENT_OPTIONS
        msg = into_data_pasajero_client_menu(context)
        update.callback_query.message.edit_text(text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
        return CLIENT_INTO_DATA_PASS
    elif query == "no" or query == "atras":
        return new_client_callback_query(update, context)
    else:
        return cancel(update, context)

def save_data(context):
    context.user_data['all_passeger'].append([context.user_data['passeger_name'], context.user_data['passeger_last_name'], context.user_data['passeger_country'], context.user_data['passeger_no_passport']])

def name_passeger_message_text(update, context):
    context.user_data['passeger_name'] = update.message.text
    update.message.delete()
    msg = into_data_pasajero_client_menu(context)
    msg[0] = data_passeger_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_INTO_DATA_PASS

def last_name_passeger_message_text(update, context):
    context.user_data['passeger_last_name'] = update.message.text
    update.message.delete()
    msg = into_data_pasajero_client_menu(context)
    msg[0] = data_passeger_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_INTO_DATA_PASS

def no_passport_passeger_message_text(update, context):
    no_passport = update.message.text
    update.message.delete()
    context.user_data['passeger_no_passport'] = no_passport
    msg = into_data_pasajero_client_menu(context)
    msg[0] = data_passeger_client_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_INTO_DATA_PASS

def client_cant_pasajeros_message_text(update, context):
    cant = update.message.text
    update.message.delete()
    if not cant.isdigit() or  int(cant) == 0:
        msg = "Introduzca la cantidad de pasajes a reservar. \n\n🚫Por favor introduzca solo la cantidad de pasajes a revervar🚫"
        try:
            update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg, parse_mode = 'Markdown')
        except:
            pass
        return CLIENT_CANT_PASAJES

    result = select_passengers_count(context, int(cant))
    if result != []: 
        context.user_data['cant_pasajes'] = int(cant)
    else:
        context.bot.answer_callback_query(context.user_data['id_query'], text="🚫No hay capacidad para la cantidad de pasajes introducidos.🚫")

    msg = make_prebooking_client_menu()
    msg[0] = data_client_prebooking_refresh(msg[0], context)
    update.message.bot.edit_message_text(chat_id=update.message.chat_id, message_id=context.user_data['message_id'], text=msg[0], parse_mode = 'Markdown', reply_markup=msg[1])
    return CLIENT_MAKE_PREBOOKING

def data_client_prebooking_refresh(msg, context):
    if context.user_data['cant_pasajes'] != "":
        msg += f"\n Cantidad de Reservas: {context.user_data['cant_pasajes']}"

    if context.user_data['origen'] != "":
        msg += f"\n Lugar de Origen: {select_name_aeroport(context.user_data['origen'])[0][0]}"

    if context.user_data['destino'] != "":
        msg += f"\n Lugar de Destino: {select_name_aeroport(context.user_data['destino'])[0][0]}"

    if context.user_data['aerolinea'] != "":
        msg += f"\n Aerolinea: {select_name_aeroline(context.user_data['aerolinea'])[0][0]}"

    if context.user_data['fecha'] != "":
        msg += f"\n Fecha de Salida: {context.user_data['fecha']}"
    return msg

def initialize_client_prebooking(context):
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
