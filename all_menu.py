import buttons
import telegram

from select_from_table import *
from buttons import *

def for_user_type_unknown_menu(name):
    msg = f"Hola {name}, que tipo de usuario quiere ser de este bot??"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cliente", callback_data="new_client"))
    button_list.append(telegram.InlineKeyboardButton("Empleado", callback_data="new_employee"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    return [msg,reply_markup]  

def for_user_type_start_menu(user_type, name):
    msg = f"Hola {name}, que desea hacer?"
    button_list = []
    reply_markup = None 
    if user_type == "client":
        button_list.append(telegram.InlineKeyboardButton("Prereservas", callback_data="prereserva_client"))
        #button_list.append(telegram.InlineKeyboardButton("Ver vuelos disponibles", callback_data="vuelos_disp_client"))
        button_list.append(telegram.InlineKeyboardButton("Ver mis vuelos futuros", callback_data="vuelos_fut_client"))
        button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
        reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))

    employee = user_type.split('_')
    if employee[0] == "employee":
        #Gerente de ventas
        if employee[1] == "salesManager":
            button_list.append(telegram.InlineKeyboardButton("Pasajes", callback_data="pasajes_gv"))
            button_list.append(telegram.InlineKeyboardButton("Prereservas", callback_data="prereserva_gv"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de mostrador
        elif employee[1] == "counter":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Vuelo", switch_inline_query_current_chat=".v "))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de migracion
        elif employee[1] == "immigration":
            button_list.append(telegram.InlineKeyboardButton("Control de Entrada", switch_inline_query_current_chat=".ce "))
            button_list.append(telegram.InlineKeyboardButton("Control de Salida", switch_inline_query_current_chat=".cs "))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de puerta de salida
        elif employee[1] == "exitDoor":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Vuelo", switch_inline_query_current_chat=".ved "))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Operador de vuelo
        elif employee[1] == "flightOperator":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Nave", switch_inline_query_current_chat=".nfl "))
            button_list.append(telegram.InlineKeyboardButton("Programacion", callback_data="programacion"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Recursos Humanos
        elif employee[1] == "humanResources":
            button_list.append(telegram.InlineKeyboardButton("Empleados", callback_data="empleados"))
            button_list.append(telegram.InlineKeyboardButton("Añadir Empleados", callback_data="añadir_empleados"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Mecanica
        elif employee[1] == "chiefMachanic":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Nave", switch_inline_query_current_chat=".n "))
            button_list.append(telegram.InlineKeyboardButton("Añadir Nave", callback_data="añadir_nave"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Almacen
        elif employee[1] == "warehouseManager":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Producto", switch_inline_query_current_chat=".prwg "))
            button_list.append(telegram.InlineKeyboardButton("Añadir Producto", callback_data="añadir_producto"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Supervisor de Instalaciones
        elif employee[1] == "facilitiesSupervisor":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Instalacion", switch_inline_query_current_chat=".i "))
            button_list.append(telegram.InlineKeyboardButton("Añadir Instalacion", callback_data="añadir_instalacion"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de una instalacion
        elif employee[1] == "installation":
            button_list.append(telegram.InlineKeyboardButton("Compra", callback_data="compra"))
            button_list.append(telegram.InlineKeyboardButton("Almacen", callback_data="almacen"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def client_registration_menu(name):
    msg = f"{name}, Por favor ingrese sus datos personales para registrarse en el bot. \n"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre", show_alert=True))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))
    button_list.append(telegram.InlineKeyboardButton("Pais", callback_query="pais", switch_inline_query_current_chat=".pc "))
    button_list.append(telegram.InlineKeyboardButton("No_pasaporte", callback_data="no_pasaporte"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def client_registration_refresh_menu(name, context):
    msg = f"{name}, Por favor ingrese sus datos personales para registrarse en el bot. \n"
    if context.user_data['name'] != "":
        msg += f"\n Nombre: {context.user_data['name']}"

    if context.user_data['last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['last_name']}"

    if context.user_data['country'] != "":
        msg += f"\n Country: {context.user_data['country']}"

    if context.user_data['no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['no_passport']}"
    
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre", show_alert=True))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))
    button_list.append(telegram.InlineKeyboardButton("Pais", callback_query="pais", switch_inline_query_current_chat=".pc "))
    button_list.append(telegram.InlineKeyboardButton("No_pasaporte", callback_data="no_pasaporte"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def save_data_client_menu(context):
    msg = "Esta seguro que esta informacion es correcta?\n"
    msg+= "\n Nombre: " + context.user_data['name']
    msg+= "\n Apellidos: " + context.user_data['last_name']
    msg+= "\n Pais: " + context.user_data['country']
    msg+= "\n No Pasaporte: " + context.user_data['no_passport']
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("SI", callback_data="si"))
    button_list.append(telegram.InlineKeyboardButton("NO", callback_data="no"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    cancel = telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar")
    reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=2, footer_buttons=[cancel])) 
    return [msg,reply_markup]

def save_data_passenger_client_menu(context):
    msg = "Esta seguro que esta informacion es correcta?\n"
    msg+= "\n Nombre: " + context.user_data['passeger_name']
    msg+= "\n Apellidos: " + context.user_data['passeger_last_name']
    msg+= "\n Pais: " + context.user_data['passeger_country']
    msg+= "\n No Pasaporte: " + str(context.user_data['passeger_no_passport'])
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("SI", callback_data="si"))
    button_list.append(telegram.InlineKeyboardButton("NO", callback_data="no"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    cancel = telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar")
    reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=2, footer_buttons=[cancel])) 
    return [msg,reply_markup]

def save_data_owner_client_menu(context):
    msg = "Esta seguro que esta informacion es correcta?\n"
    msg+= "\n Nombre: " + context.user_data['owner_name']
    msg+= "\n Apellidos: " + context.user_data['owner_last_name']
    msg+= "\n Pais: " + context.user_data['owner_country']
    msg+= "\n No Pasaporte: " + str(context.user_data['owner_no_passport'])
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("SI", callback_data="si"))
    button_list.append(telegram.InlineKeyboardButton("NO", callback_data="no"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    cancel = telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar")
    reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=2, footer_buttons=[cancel])) 
    return [msg,reply_markup]

def into_data_pasajero_client_menu(context):
    msg = f"Por favor introduzca los datos del pasajero {context.user_data['index']}"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre"))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))
    button_list.append(telegram.InlineKeyboardButton("Pais", callback_query="pais", switch_inline_query_current_chat=".pp "))
    button_list.append(telegram.InlineKeyboardButton("No_pasaporte", callback_data="no_pasaporte"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def into_data_owner_client_menu(context):
    msg = f"Por favor introduzca los datos de la persona a quien va a estar a nombre la reserva."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre"))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))
    button_list.append(telegram.InlineKeyboardButton("Pais", callback_query="pais", switch_inline_query_current_chat=".po "))
    button_list.append(telegram.InlineKeyboardButton("No_pasaporte", callback_data="no_pasaporte"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def employee_facilitiesSupervisor_refresh_menu(item):
    msg = "Nombre: "+str(item[0])+"\nTipo: "+str(item[1])
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def employee_facilitiesSupervisor_add_refresh_menu(context):
    msg = "Nombre: "+context.user_data["inst_name"]+"\nTipo: "+context.user_data["tipo_inst"]
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="name"))
    button_list.append(telegram.InlineKeyboardButton("Seleccionar Tipo", switch_inline_query_current_chat=".it "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]    

def into_data_pasajero_refresh_client_menu(context):
    msg = f"Por favor introduzca los datos del pasajero {context.user_data['index']}"
    if context.user_data['passeger_name'] != "":
        msg += f"\n Nombre: {context.user_data['passeger_name']}"

    if context.user_data['passeger_last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['passeger_last_name']}"

    if context.user_data['passeger_country'] != "":
        msg += f"\n Country: {context.user_data['passeger_country']}"

    if context.user_data['passeger_no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['passeger_no_passport']}"

    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre"))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))
    button_list.append(telegram.InlineKeyboardButton("Pais", callback_query="pais", switch_inline_query_current_chat=".pp "))
    button_list.append(telegram.InlineKeyboardButton("No_pasaporte", callback_data="no_pasaporte"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def into_data_owner_refresh_client_menu(context):
    msg = f"Por favor introduzca los datos de la persona a nombre de quien va a estar la reserva "
    if context.user_data['owner_name'] != "":
        msg += f"\n Nombre: {context.user_data['owner_name']}"

    if context.user_data['owner_last_name'] != "":
        msg += f"\n Apellidos: {context.user_data['owner_last_name']}"

    if context.user_data['owner_country'] != "":
        msg += f"\n Country: {context.user_data['owner_country']}"

    if context.user_data['owner_no_passport'] != "":
        msg += f"\n NoPassport: {context.user_data['owner_no_passport']}"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre"))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))
    button_list.append(telegram.InlineKeyboardButton("Pais", callback_query="pais", switch_inline_query_current_chat=".po "))
    button_list.append(telegram.InlineKeyboardButton("No_pasaporte", callback_data="no_pasaporte"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  

def prebooking_client_menu():
    msg = "Que desea hacer?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Ver mis preservas", callback_data="ver_prereservas"))
    button_list.append(telegram.InlineKeyboardButton("Realizar preserva", callback_data="realizar_prereserva"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def make_prebooking_client_menu():
    msg = "Rellene todos los campos para hacer efectiva su prereserva."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cantidad de Pasajeros", callback_data="cant_pasajeros"))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Origen", switch_inline_query_current_chat=".lo "))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Destino", switch_inline_query_current_chat=".ld "))
    button_list.append(telegram.InlineKeyboardButton("Aerolinea", switch_inline_query_current_chat=".a "))
    button_list.append(telegram.InlineKeyboardButton("Fecha de Salida", switch_inline_query_current_chat=".fs "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def make_prebooking_client_refresh_menu(context):
    msg = "Rellene todos los campos para hacer efectiva su prereserva."

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

    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cantidad de Pasajeros", callback_data="cant_pasajeros"))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Origen", switch_inline_query_current_chat=".lo "))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Destino", switch_inline_query_current_chat=".ld "))
    button_list.append(telegram.InlineKeyboardButton("Aerolinea", switch_inline_query_current_chat=".a "))
    button_list.append(telegram.InlineKeyboardButton("Fecha de Salida", switch_inline_query_current_chat=".fs "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def save_prebooking_client_menu(context):
    msg = f"Esta seguro que esta informacion es correcta?\n"
    msg+= f"\n Cantidad de Reservas: {context.user_data['cant_pasajes']}"
    msg+= f"\n Lugar de Origen: {select_name_aeroport(context.user_data['origen'])[0][0]}"
    msg+= f"\n Lugar de Destino: {select_name_aeroport(context.user_data['destino'])[0][0]}"
    msg+= f"\n Aerolinea: {select_name_aeroline(context.user_data['aerolinea'])[0][0]}"
    msg+= f"\n Fecha de Salida: {context.user_data['fecha']}"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("SI", callback_data="si"))
    button_list.append(telegram.InlineKeyboardButton("NO", callback_data="no"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    cancel = telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar")
    reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=2, footer_buttons=[cancel])) #DUDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    return [msg,reply_markup]  

def new_employee_options():
    msg = "Si usted es un nuevo empleado, por favor introduzca su codigo de verificacion."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Codigo de Verificacion", callback_data="code"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def new_employee_verification_code():
    msg = "Introduzca su codigo de verificacion."
    return [msg,None]

def employee_list_menu():
    msg = "Elija el empleado que desea comprobar."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Empleados", switch_inline_query_current_chat=".e "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_add_menu():
    msg = "Ingrese los datos del nuevo empleado."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Numero de carnet", callback_data="carnet"))
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre"))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))     
    button_list.append(telegram.InlineKeyboardButton("Cargo", switch_inline_query_current_chat=".c "))
    button_list.append(telegram.InlineKeyboardButton("Instalacion", switch_inline_query_current_chat=".ih "))
    button_list.append(telegram.InlineKeyboardButton("Pais", switch_inline_query_current_chat=".phr "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]


def employee_chiefMachanic_add_nave_menu(context):
    msg = "Introduzca los datos de la nave a añadir."
    if context.user_data['matricula'] != "":
        msg += f"\nNombre: {context.user_data['matricula']}"
    if context.user_data['capacidad'] != "":
        msg += f"\nCapacidad: {context.user_data['capacidad']}"
    if context.user_data['tipo'] != "":
        msg += f"\nTipo: {context.user_data['tipo']}"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Matricula", callback_data="matricula"))
    button_list.append(telegram.InlineKeyboardButton("Capacidad", callback_data="capacidad"))
    button_list.append(telegram.InlineKeyboardButton("Clasificacion", callback_data="tipo"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
    return [msg,reply_markup]  


def employee_add_refresh_menu(context):
    msg = "Ingrese los datos del nuevo empleado."
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
    if context.user_data["ID_I"] != "":
        msg += f"\nInstalacion: {context.user_data['ID_I']}"

    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Numero de carnet", callback_data="carnet"))
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="nombre"))
    button_list.append(telegram.InlineKeyboardButton("Apellidos", callback_data="apellidos"))     
    button_list.append(telegram.InlineKeyboardButton("Cargo", switch_inline_query_current_chat=".c "))
    button_list.append(telegram.InlineKeyboardButton("Instalacion", switch_inline_query_current_chat=".ih "))
    button_list.append(telegram.InlineKeyboardButton("Pais", switch_inline_query_current_chat=".phr "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_immigration_fligth_menu():
    msg = "Seleccione el vuelo que desea chequear."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Chequear Vuelo", switch_inline_query_current_chat=".ed "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_immigration_passa_menu():
    msg = "Seleccione el pasajero que desea chequear."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Chequear Pasajelo", switch_inline_query_current_chat=".pa "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]    

def employee_facilitiesSupervisior_add_inst_menu():
    msg = "Introduzca los datos de la instalacion a añadir."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="name"))
    button_list.append(telegram.InlineKeyboardButton("Seleccionar Tipo", switch_inline_query_current_chat=".it "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]    

def employee_warehouseManager_add_prod_menu():
    msg = "Introduzca los datos del producto a añadir."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Nombre", callback_data="name_prod"))
    button_list.append(telegram.InlineKeyboardButton("Cantidad", callback_data="cant"))
    button_list.append(telegram.InlineKeyboardButton("Precio", callback_data="precio"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_humanResources_info_menu(item):
    msg = "Informacion del empleado\n"
    msg += "ID de Empleado: " + str(item[2]) + '\n' 
    msg += "No de Carnet: " + str(item[4]) + '\n' 
    msg += "Nombre: "+item[0]+" "+item[1]+'\n'
    msg += "Pais: "+item[3]+'\n'
    msg += "Cargo: " + item[5]
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Eliminar", callback_data="eliminar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_1"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]


#def employee_warehouseManager_add_prod_menu():
#    msg = "Como desea ver la lista de pasajeros del vuelo seleccionado."
#    button_list = []
#    button_list.append(telegram.InlineKeyboardButton("Ver listado completo", callback_data="list_compl"))
#    button_list.append(telegram.InlineKeyboardButton("Ver cliente por cliente", callback_data="client_to_client"))
#    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
#    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
#    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
#    return [msg,reply_markup]

def employee_warehouseManager_completeList_menu(msg):
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_installation_purchases_menu():
    msg = "Introduzca los datos de la compra."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Codigo del Producto", switch_inline_query_current_chat=".prb "))
    button_list.append(telegram.InlineKeyboardButton("Cantidad", callback_data="cant"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_installation_purchases_refresh_menu(context):
    msg = "Introduzca los datos de la compra."
    msg += f"\nCodigo: {context.user_data['codigo_prod']}"
    msg += f"\nCantidad: {context.user_data['cant_prod']}"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Codigo del Producto", switch_inline_query_current_chat=".prb "))
    button_list.append(telegram.InlineKeyboardButton("Cantidad", callback_data="cant"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_installation_wareHouse_menu():
    msg = "Que producto desea revisar?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Productos", switch_inline_query_current_chat=".pr "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_installation_wareHouse_info_prod_menu(item):
    msg = "ID: "+str(item[0])
    msg += "\nNombre: "+item[1]
    msg += "\nCantidad: "+str(item[3])
    msg += "\nPrecio: "+str(item[2])
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]


#def employee_counter_menu1(name):
#    msg = f"Hola {name}, que desea hacer?"
#    button_list = []
#    button_list.append(telegram.InlineKeyboardButton("Seleccionar Vuelo", switch_inline_query_current_chat="edm "))
#    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
#    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
#    return [msg,reply_markup]    

def employee_counter_menu2():
    msg = "Seleccione un cliente a verficar.\n"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Seleccionar Cliente", switch_inline_query_current_chat=".cm "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_1"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]    

def employee_counter_menu3(item):
    msg = "**Datos del pasajero**\n\n"
    msg += "No Pasaporte: "+item[3]+'\n'
    msg += "Nombre: "+item[0]+" "+item[1]+'\n'
    msg += "Pais: "+item[2]
    msg += "\n\n**Detalles del pasaje**"+'\n\n'
    msg += "Codigo del vuelo: "+str(item[6])+'\n'
    msg += "Aerolinea: "+item[9]+'\n'
    msg += "Aeropuerto de Origen: "+item[10]+'\n'
    msg += "Fecha de Salida: "+item[7].isoformat(' ')+'\n'
    msg += "Aeropuerto de Llegada: "+item[11]+'\n'
    msg += "Fecha de Llegada: "+item[8].isoformat(' ')+'\n'
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cantidad de maletas", callback_data="cantMaletas"))
    button_list.append(telegram.InlineKeyboardButton("Check it", callback_data="check"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_2"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]   

def employee_salesManager_pasajes_menu():
    msg = "Que desea hacer?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Vender Pasajes", callback_data="vender_pasaje"))
    #button_list.append(telegram.InlineKeyboardButton("Modificar Pasajes", callback_data="mod_pasaje"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup] 

def employee_salesManager_prereserva_menu():
    msg = "Que desea hacer?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Ver las prereservas vigentes", callback_data="prereserva_vigentes"))
    button_list.append(telegram.InlineKeyboardButton("Pago de prereservas", callback_data="pago_prereseva"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_salesManager_prereserva_view_menu(item):
    msg = "\n\n**Detalles de reserva**"+'\n\n'
    msg += "ID de la Reserva " + str(item[0])+'\n'
    msg += "ID de Cliente: " + str(item[1])+'\n'
    msg += "Fecha de la reserva: " + str(item[3])+'\n'
    msg += "\n\n**Detalles del pasaje**"+'\n\n'
    msg += "Codigo del vuelo: "+str(item[4])+'\n'
    msg += "Aeropuerto de Origen: "+item[5]+'\n'
    msg += "Fecha de Salida: "+item[6].isoformat(' ')+'\n'
    msg += "Aeropuerto de Llegada: "+item[7]+'\n'
    msg += "Fecha de Llegada: "+item[8].isoformat(' ')+'\n'
    msg += "Precio: " +str(item[9]) +'\n'

    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Pagado", callback_data="pagado"))
    button_list.append(telegram.InlineKeyboardButton("Eliminar", callback_data="eliminar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_salesManager_prereserva_code_menu():
    msg = "Cual es el codigo de la prereserva?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Codigo", switch_inline_query_current_chat=".cod "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def make_presell_menu():
    msg = "Rellene todos los campos para hacer efectiva la venta."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cantidad de Pasajeros", callback_data="cant_pasajeros"))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Origen", switch_inline_query_current_chat=".logv "))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Destino", switch_inline_query_current_chat=".ldgv "))
    button_list.append(telegram.InlineKeyboardButton("Aerolinea", switch_inline_query_current_chat=".agv "))
    button_list.append(telegram.InlineKeyboardButton("Fecha de Salida", switch_inline_query_current_chat=".fsgv "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def modif_pasaje_menu():
    msg = "Introduzca el numero de pasaporte."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("No Pasaporte", switch_inline_query_current_chat=".np "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_1"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def pasaje_futuro_menu():
    msg = "Pasajes futuros del cliente."
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Pasajes", switch_inline_query_current_chat=".cp "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_2"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def modif_all_options_menu():
    msg = "Que desea modificar?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Lugar de Origen", switch_inline_query_current_chat=".logv "))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Destino", switch_inline_query_current_chat=".ldgv "))
    button_list.append(telegram.InlineKeyboardButton("Aerolinea", switch_inline_query_current_chat=".agv "))
    button_list.append(telegram.InlineKeyboardButton("Fecha de Salida", switch_inline_query_current_chat=".fsgv "))
    button_list.append(telegram.InlineKeyboardButton("Guardar cambios", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_3"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def make_prebooking_salesManager_refresh_menu(context):
    msg = "Rellene todos los campos para hacer efectiva su prereserva."

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

    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Cantidad de Pasajeros", callback_data="cant_pasajeros"))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Origen", switch_inline_query_current_chat=".logv "))
    button_list.append(telegram.InlineKeyboardButton("Lugar de Destino", switch_inline_query_current_chat=".ldgv "))
    button_list.append(telegram.InlineKeyboardButton("Aerolinea", switch_inline_query_current_chat=".agv "))
    button_list.append(telegram.InlineKeyboardButton("Fecha de Salida", switch_inline_query_current_chat=".fsgv "))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_flightOperator_flight_selected(item):
    msg = item[0]+'\n'+"Tipo: "+item[1]+'\n'+"Capacidad: "+str(item[2])+'\n'+"Numeros de tripulantes a bordo: "+str(item[3])
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_flightOperator_prog_flight_selected(item):
    msg = item[1]+'\n'+"Codigo de Vuelo: "+str(item[0])+'\n'+"Aerolinea: "+item[2]
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_flightOperator_prog():
    msg = "Que tipo de vuelos desea ver?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Entrada", switch_inline_query_current_chat=".ne "))
    button_list.append(telegram.InlineKeyboardButton("Salida", switch_inline_query_current_chat=".ns "))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]


def employee_exitDoor_passenger_list_menu():
    msg = "Como desea ver la lista de pajeros del vuelo seleccionado?"
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Ver listado completo", callback_data="list_compl"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_exitDoor_complete_list_menu(msg):
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_immigration_passenger_menu(item):
    msg = item[3]+'\n'+"Nombre: "+item[0]+item[1]+'\n'+"Pais: "+item[2]
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Aceptar", callback_data="aceptar"))
    button_list.append(telegram.InlineKeyboardButton("Denegar", callback_data="denegar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

def employee_chiefMachanic_refresh_menu(info_n, repair):
    msg = info_n[0]
    msg += "\nTipo: "+info_n[1]
    msg += "\nCapacidad: "+str(info_n[2])
    msg += '\n'
    msg += "-"*50
    msg += "\nDetalles de las reparaciones\n"
    if len(repair) == 0:
        msg += "No hay reparaciones a mostrar."
    else:# a partir de aqui esta las reparaciones
        for item in repair:
            msg += "\nFecha de inicio: " + str(item[1])
            msg += "\nFecha de finalizacion: " + str(item[2])
            msg += "\nTipo de reparacion general: " + str(item[3])
            msg += "\nCosto de la reparacion general: " + str(item[4])
            msg += "\nTipo de reparacion especifica: " + str(item[8])
            msg += "\nCosto de la reparacion especifica: " + str(item[5])
            msg += "\nMonto total de la reparacion general: " + str(item[6])
            msg += '\n'
            msg += "-"*50

    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Añadir Reparacion", callback_data="add_repair"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_1"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]


def employee_chiefMachanic_add_repair_refresh_menu(context):
    msg = "Detalles de la nueva reparacion."
    if context.user_data['repair'] != []:
        msg += "\nCodigo de la reparacion: "+str(context.user_data['repair'][0])
        msg += "\nTipo de reparacion: "+context.user_data['repair'][1]
        msg += "\nPrecio: "+str(context.user_data['repair'][2])
    if context.user_data['days'] != "":
        msg += "\nDuracion: "+str(context.user_data['days'])+("dia" if int(context.user_data['days']) <= 1 else "dias")
    button_list = []
    button_list.append(telegram.InlineKeyboardButton("Tipo de Reparacion", switch_inline_query_current_chat=".rp "))
    button_list.append(telegram.InlineKeyboardButton("Duracion", callback_data="duracion"))
    button_list.append(telegram.InlineKeyboardButton("Guardar", callback_data="guardar"))
    button_list.append(telegram.InlineKeyboardButton("Atras", callback_data="atras_2"))
    button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancelar"))
    reply_markup = telegram.InlineKeyboardMarkup(build_menu(button_list, n_cols=1))
    return [msg,reply_markup]

