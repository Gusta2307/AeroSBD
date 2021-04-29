import buttons
import telegram

def message_menu(user_type, name):
    msg = f"Hola {name}, que desea hacer?"
    button_list = []
    reply_markup = None
    if user_type == "client":
        button_list.append(telegram.InlineKeyboardButton("Prereservas", callback_data="prereserva_client"))
        button_list.append(telegram.InlineKeyboardButton("Ver vuelos disponibles", callback_data="vuelos_disp_client"))
        button_list.append(telegram.InlineKeyboardButton("Ver mis vuelos futuros", callback_data="vuelos_ fut_client"))
        button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
        reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        
    employee = user_type.split('_')
    if employee[0] == "Empleado":
        #Gerente de ventas
        if employee[1] == "Gerente de ventas":
            button_list.append(telegram.InlineKeyboardButton("Pasajes", callback_data="pasajes_gv"))
            button_list.append(telegram.InlineKeyboardButton("Prereservas", callback_data="prereserva_gv"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de mostrador
        elif employee[1] == "mostrador":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Vuelo", switch_inline_query_current_chat="v. "))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de migracion
        elif employee[1] == "migracion":
            button_list.append(telegram.InlineKeyboardButton("Control de Entrada", callback_data="contro_ent_em"))
            button_list.append(telegram.InlineKeyboardButton("Control de Salida", callback_data="contro_sal_em"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Empleado de puerta de salida
        elif employee[1] == "puerta de salida":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Vuelo", switch_inline_query_current_chat="v. "))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Operador de vuelo
        elif employee[1] == "Opedador de vuelo":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Nave", switch_inline_query_current_chat="n. "))
            button_list.append(telegram.InlineKeyboardButton("Programacion", callback_data="programacion"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Recursos Humanos
        elif employee[1] == "Jefe de Recursos Humanos":
            button_list.append(telegram.InlineKeyboardButton("Empleados", callback_data="empleados"))
            button_list.append(telegram.InlineKeyboardButton("Añadir Empleados", callback_data="añadir_empleados"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Mecanica
        elif employee[1] == "Jefe de Mecanica":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Nave", switch_inline_query_current_chat="n. "))
            button_list.append(telegram.InlineKeyboardButton("Añadir Nave", callback_data="añadir_empleados"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Almacen
        elif employee[1] == "Jefe de Almacen":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Producto", switch_inline_query_current_chat="p. "))
            button_list.append(telegram.InlineKeyboardButton("Añadir Producto", callback_data="añadir_producto"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Supervisor de Instalaciones
        elif employee[1] == "Jefe de Supervisor de Instalaciones":
            button_list.append(telegram.InlineKeyboardButton("Seleccionar Instalacion", switch_inline_query_current_chat="i. "))
            button_list.append(telegram.InlineKeyboardButton("Añadir Instalacion", callback_data="añadir_instalacion"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
        #Jefe de Supervisor de Instalaciones
        elif employee[1] == "Jefe de Supervisor de Instalaciones":
            button_list.append(telegram.InlineKeyboardButton("Compra", callback_data="compra"))
            button_list.append(telegram.InlineKeyboardButton("Almacen", callback_data="almacen"))
            button_list.append(telegram.InlineKeyboardButton("Cancelar", callback_data="cancel"))
            reply_markup = telegram.InlineKeyboardMarkup(buttons.build_menu(button_list, n_cols=1))
    return [msg,reply_markup]
