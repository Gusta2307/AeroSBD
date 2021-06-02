import logging
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, InlineQueryHandler, Filters, ConversationHandler, CallbackQueryHandler,ChosenInlineResultHandler, CallbackContext 
from telegram import InlineQueryResultArticle, InputTextMessageContent, User, CallbackQuery
from random import getrandbits

import os
import psycopg2

import create_table
import insert_table
import contains
import employee

from employee import *
from create_table import *
from insert_table import *
from all_menu import *
from buttons import *
from tags import *
from client import *
from employee_human_resources import *
from select_from_table import *
from cargo import *
from countries import *
from employee_immigration import *
from employee_facilitiesSupervisor import *
from employee_warehouseManager import *
from employee_exitDoor import *
from employee_flightOperator import *
from employee_chiefMachanic import *
from employee_installation import *
from employee_counter import *
from employee_salesManager import *
from insert_data import *

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(update):
        update.start_polling()
        update.idle()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
        updater.bot.set_webhook("https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}")

def start(update, context, is_back=False): #Metodo que se ejecuta cuando se activa el comando start
    #Comprobamos si el usuario ya esta registrado en el bot 
    user_type = employee.select_job(contains.isRegistered(update.effective_user['id']))
    name = update.effective_user['first_name']
    logger.info("El usuario {0}, ha iniciado el bot".format(name))
    message_id = None
    if user_type == "": #Si no esta registrado preguntamos si es cliente o empleado
        message = for_user_type_unknown_menu(name)
        if not is_back:
            message_id = update.message.chat.send_message(text=message[0], parse_mode = 'Markdown', reply_markup=message[1]).message_id
            context.user_data['message_id'] = message_id
        else:
            update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])
    else:
        message = for_user_type_start_menu(user_type, name)
        if not is_back:
            message_id = update.message.chat.send_message(text=message[0], parse_mode = 'Markdown', reply_markup=message[1]).message_id
            context.user_data['message_id'] = message_id
        else:
            update.callback_query.message.edit_text(text=message[0], parse_mode = 'Markdown', reply_markup=message[1])  

        return select_tags(user_type, context)

    return START

def select_tags(user_type, context):
    if user_type == "client":
        return CLIENT_OPTIONS
    elif user_type == "employee_humanResources":
        return EMPLOYEE_HUMAN_RESOURCES
    elif user_type == "employee_chiefMachanic":
        initialize_nave(context)
        return EMPLOYEE_CHIEFMACHANIC
    elif user_type == "employee_exitDoor":
        context.user_data['flight'] = ""
        return EMPLOYEE_EXITDOOR
    elif user_type == "employee_facilitiesSupervisor":
        return EMPLOYEE_FACILITIESSUPERVISOR
    elif user_type == "employee_immigration":
        return EMPLOYEE_IMMIGRATION
    elif user_type == "employee_installation":
        return EMPLOYEE_INSTALLATION
    elif user_type == "employee_warehouseManager":
        return EMPLOYEE_WAREHOUSEMANGER
    elif user_type == "employee_counter":
        initialize_employee_counter(context)
        return EMPLOYEE_COUNTER
    elif user_type == "employee_salesManager":
        return EMPLOYEE_SALESMANAGER
    elif user_type == "employee_flightOperator":
        return EMPLOYEE_FLIGHTOPERATOR


def start_callback_query(update, context):
    query = update.callback_query.data
    if query == "new_client":
        return new_client_callback_query(update, context)
    elif query == "new_employee":
        return new_employee_callback_query(update, context)
    else:
        return cancel(update, context)

def cancel(update, context):
    logger.info("El usuario {0}, cancel".format(update.effective_user['first_name']))
    update.callback_query.message.delete()
    return ConversationHandler.END

def inline(bot, update):
    query = bot.inline_query.query
    print(bot.inline_query.id)
    id = bot.inline_query.id
    index = 0
    resultados = list()
    if query.startswith(".pc") or query.startswith(".phr") or query.startswith(".pp") or query.startswith(".po"):
        #resultados = list()
        text = None
        if query.startswith(".pc"):
            text = query.replace(".pc", "").strip() 
        elif query.startswith(".phr"):
            text = query.replace(".phr", "").strip()
        elif query.startswith(".pp"):
            text = query.replace(".pp", "").strip()
        elif query.startswith(".po"):
            text = query.replace(".po", "").strip()
        all_countries = get_country()
        countries = []
        if text == "":
            for c in all_countries:
                countries.append(c)
        else:
            for c in all_countries:
                if c['name'].lower().find(text.lower()) != -1:
                    countries.append(c)
                    
        countries_temp = []

        for c in countries:
            countries_temp.append(c['name'])
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=c['name'],
                input_message_content=InputTextMessageContent(message_text=c['name'], parse_mode = 'Markdown'),
                thumb_url="https://www.countryflags.io/{0}/shiny/64.png".format(c['code']),
                description="Capital: {0} \nContinente: {1}".format(c['capital'], c['continent']),
            ))
            index+=1
            if index == 50: #Maximo numero de resultado que se acepta
                break
        update.user_data['list_countries'] = countries_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".e"):
        #resultados = list()
        text = query.replace(".e", "").strip()
        all_employee = select_all_employee_in_aeroports(select_ID_A_employee_using_id_telegram(bot.effective_user['id'])[0])
        employees = []
        if text == "":
            employees = all_employee

        else:
            for item in all_employee:
                if item[1].lower().find(text.lower()) != -1 or item[2].lower().find(text.lower()) != -1 or str(item[4]).find(text) != -1 or item[5].lower().find(text.lower()) != -1:
                    employees.append(item)

        for item in employees:
            resultados.append(InlineQueryResultArticle(
                id=index,
                title="ID: "+str(item[2]),
                input_message_content=InputTextMessageContent(message_text=str(item[2])),
                thumb_url="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png",
                description="Nombre: {0} \nPuesto de Trabajo: {1}".format(str(item[0]) + " " + str(item[1]), str(item[5]))),
            )
            index+=1
            if index == 50: #Maximo numero de resultado que se acepta
                break
        update.user_data['list_employees'] = employees
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".ce") or query.startswith(".cs"):
        #resultados = list()
        if query.startswith(".ce"):
            text = query.replace(".ce", "").strip()
            list_c = select_all_passengers_in(bot.effective_user['id'])
        elif query.startswith(".cs"):
            text = query.replace(".cs", "").strip()
            list_c = select_all_passengers_on(bot.effective_user['id'])
        
        list_c_temp = []
        if text != "":
            for item in list_c:
                if item[0].lower().find(text.lower()) != -1 or item[1].lower().find(text.lower()) != -1 or item[3].find(text) != -1:
                    list_c_temp.append(item)
        else:
            list_c_temp = list_c
        for item in list_c_temp:
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=str(item[3]),
                input_message_content=InputTextMessageContent(message_text=item[0]),
                thumb_url="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png",
                description="Nombre: "+item[0]+" "+item[1]+'\n'+"Pais: "+item[2]),
            )
            index += 1
        update.user_data['list_c'] = list_c_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".cm"):
        #resultados = list()
        text = query.replace(".cm", "").strip()
        list_cm = select_all_passengers_in_flight(update.user_data["ID_F"])
        list_cm_temp = []
        if text != "":
            for item in list_cm:
                if item[1].lower().find(text.lower()) != -1:
                    list_cm_temp.append(item)
        else:
            list_cm_temp = list_cm
        
        for item in list_cm_temp:
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[0],
                input_message_content=InputTextMessageContent(message_text=item[0]),
                thumb_url="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png",
                description=None),
            )
            index += 1
        update.user_data['list_cm'] = list_cm_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".cod"):
        #resultados = list()
        text = query.replace(".cod", "").strip()
        list_cod = select_Booking_not_paid()
        #ID_B, ID_C, ID_F, Date_booking, Cod_F, a_s, Date_Hour_S, Name_AeroP as a_l, Date_Hour_L, Price
        list_cod_temp = []
        if text != "":
            for item in list_cod:
                if item[0].lower().find(text.lower()) != -1:
                    list_cod_temp.append(item)
        else:
            list_cod_temp = list_cod

        for item in list_cod_temp:
            resultados.append(InlineQueryResultArticle(
                id=index,
                title="ID: "+str(item[0]),
                input_message_content=InputTextMessageContent(message_text="ID: "+str(item[0])),
                thumb_url="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png",
                description="Lugar de salida: "+str(item[5]+"\nLugar de llegada: "+str(item[7]))),
            )
            index += 1
        update.user_data['list_cod'] = list_cod_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".c"):
        #resultados = list()
        text = query.replace(".c", "").strip()
        list_jobs = get_jobs()
        list_jobs_temp = []
        if text != "":
            for item in list_jobs:
                if item[1].lower().find(text.lower()) != -1:
                    list_jobs_temp.append(item)
        else:
            list_jobs_temp = list_jobs

        for item in list_jobs_temp:
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[0],
                input_message_content=InputTextMessageContent(message_text=item[0]),
                thumb_url="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png",
                description=None),
            )
            index += 1
        update.user_data['list_jobs'] = list_jobs_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".fs") or query.startswith(".fsgv"):
        #resultados = list()
        if query.startswith(".fsgv"):
            text = query.replace(".fsgv", "").strip()
        elif query.startswith(".fs"):
            text = query.replace(".fs", "").strip()
        print("A")
        list_date_go = select_date_go(update)
        print("B")
        list_data_go_temp = []
        if text != "":
            for item in list_date_go:
                if str(item[0].isoformat(' ')).find(text) != -1:
                    list_data_go_temp.append(item)
        else:
            list_data_go_temp = list_date_go

        for item in list_data_go_temp:
            date = str(item[0].isoformat(' ')).split(' ')
            day = "Dia: "+date[0]
            time = "Hora: "+date[1].split('-')[0]
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=day,
                input_message_content=InputTextMessageContent(message_text=day+'\n'+time),
                thumb_url="https://cdn-skill.splashmath.com/uploads/skill_detail/image/tell-time-to-quarter-hours/tell-time-to-quarter-hours.jpg",
                description=time),
            )
            index += 1
        update.user_data['list_date_go'] = list_data_go_temp
        print(list_data_go_temp)
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".ldgv") or query.startswith(".ld") :
        #resultados = list()
        if query.startswith(".ldgv"):
            text = query.replace(".ldgv", "").strip()
        elif query.startswith(".ld"):
            text = query.replace(".ld", "").strip()
        list_dest = select_airport_destination(update)
        list_dest_temp = []
        if text != "":
            for item in list_dest:
                if item[1].lower().find(text.lower()) != -1 or item[2].lower().find(text.lower()) != -1:
                    list_dest_temp.append(item)
        else:
            list_dest_temp = list_dest
        for item in list_dest_temp:
            country = "Pais: "+item[2]
            ubi = "Ubicacion: "+item[3]
            msg = item[1]+'\n'+country+'\n'+ubi
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[1],
                input_message_content=InputTextMessageContent(message_text=msg),
                thumb_url="https://cdn4.vectorstock.com/i/1000x1000/39/98/airport-signs-vector-4393998.jpg",
                description=country+'\n'+ubi),
            )
            index += 1
        update.user_data['list_dest'] = list_dest_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".logv") or query.startswith(".lo")  :
        #resultados = list()
        if query.startswith(".logv"):
            text = query.replace(".logv", "").strip()
        elif query.startswith(".lo"):
            text = query.replace(".lo", "").strip()
        list_orig = select_airport_source(update)
        list_orig_temp = []
        if text != "":
            for item in list_orig:
                if item[1].lower().find(text.lower()) != -1 or item[2].lower().find(text.lower()) != -1:
                    list_orig_temp.append(item)
        else:
            list_orig_temp = list_orig
        for item in list_orig_temp:
            country = "Pais: "+item[2]
            ubi = "Ubicacion: "+item[3]
            msg = item[1]+'\n'+country+'\n'+ubi
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[1],
                input_message_content=InputTextMessageContent(message_text=msg),
                thumb_url="https://cdn3.vectorstock.com/i/thumb-large/78/02/airport-signs-vector-4397802.jpg",
                description=country+'\n'+ubi),
            )
            index += 1
        update.user_data['list_orig'] = list_orig_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".a") or query.startswith(".agv") :
        #resultados = list()
        if query.startswith(".agv"):
            text = query.replace(".agv", "").strip()
        elif query.startswith(".a"):
            text = query.replace(".a", "").strip()
        list_aerol = select_Aeroline(update)
        list_aerol_temp = []
        if text != "":
            for item in list_aerol:
                if item[1].lower().find(text.lower()) != -1 or item[2].lower().find(text.lower()) != -1:
                    list_aerol_temp.append(item)
        else:
            list_aerol_temp = list_aerol
        for item in list_aerol_temp:
            country = "Pais: "+item[2]
            msg = item[1]+'\n'+country
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[1],
                input_message_content=InputTextMessageContent(message_text=msg),
                thumb_url="https://www.logodesignlove.com/images/airlines/lufthansa-logo.jpg",
                description=country),
            )
            index += 1
        update.user_data['list_aerol'] = list_aerol_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".nfl") or query.startswith(".ne") or query.startswith(".ns"):
        #resultados = list()
        if query.startswith(".nfl"):
            text = query.replace(".nfl", "").strip()
            list_nave = select_flight_fo(bot.effective_user['id'])
        elif query.startswith(".ne"):
            text = query.replace(".ne", "").strip()
            list_nave = select_flight_enters(bot.effective_user['id'])
        elif query.startswith(".ns"):
            text = query.replace(".ns", "").strip()
            list_nave = select_flight_departures(bot.effective_user['id'])

        list_nave_temp = []
        if text != "":
            for item in list_nave:
                if item[0].lower().find(text.lower()) != -1 or item[1].lower().find(text.lower()) != -1:
                    list_nave_temp.append(item)
        else:
            list_nave_temp = list_nave
        
        for item in list_nave_temp: 
            if query.startswith(".ne") or query.startswith(".ns"):
                msg = "Codigo de Vuelo: "+str(item[0])+'\n'+"Aerolinea: "+item[2]
            else:
                msg = "Tipo: "+item[1]+'\n'+"Capacidad: "+str(item[2])+'\n'+"Numeros de tripulantes a bordo: "+str(item[3])
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[0] if query.startswith(".nfl") else item[1],
                input_message_content=InputTextMessageContent(message_text=item[0] if query.startswith(".nfl") else item[1]),
                thumb_url="https://previews.123rf.com/images/logos2012/logos20121509/logos2012150900042/44872922-airplane-transport-concept-2d-vector-design-on-gradient-background.jpg",
                description=msg),
            )
            index += 1
        update.user_data['list_nave'] = list_nave_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".ved"):
        #resultados = list()
        text = query.replace(".ved", "").strip()
        list_vuelo = select_flight_departures_check_in_door(bot.effective_user['id'])
        list_vuelo_temp = []
        if text != "":
            for item in list_vuelo:
                if item[0].lower().find(text.lower()) != -1 or item[1].lower().find(text.lower()) != -1:
                    list_vuelo_temp.append(item)
        else:
            list_vuelo_temp = list_vuelo

        for item in list_vuelo_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[4]+" - "+item[5],
                input_message_content=InputTextMessageContent(message_text=item[4]+" - "+item[5]),
                thumb_url="https://previews.123rf.com/images/logos2012/logos20121509/logos2012150900042/44872922-airplane-transport-concept-2d-vector-design-on-gradient-background.jpg",
                description="Hora: "+item[1].isoformat(' ').split(' ')[1]+" - "+item[2].isoformat(' ').split(' ')[1]+'\n'+"Aerolinea: "+item[3]),
            )
            index += 1
        update.user_data['list_vuelo'] = list_vuelo_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".v"):
        #resultados = list()
        text = query.replace(".v", "").strip()
        list_v = select_flight_departures_check_in_door(bot.effective_user['id'])
        list_v_temp = []
        if text != "":
            for item in list_v:
                if item[0].lower().find(text.lower()) != -1 or item[1].lower().find(text.lower()) != -1:
                    list_v_temp.append(item)
        else:
            list_v_temp = list_v

        for item in list_v_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[4]+" - "+item[5],
                input_message_content=InputTextMessageContent(message_text=item[4]+" - "+item[5]),
                thumb_url="https://previews.123rf.com/images/logos2012/logos20121509/logos2012150900042/44872922-airplane-transport-concept-2d-vector-design-on-gradient-background.jpg",
                description="Hora: "+item[1].isoformat(' ').split(' ')[1]+" - "+item[2].isoformat(' ').split(' ')[1]+'\n'+"Aerolinea: "+item[3]),
            )
            index += 1
        update.user_data['list_v'] = list_v_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".n"):
        #resultados = list()
        text = query.replace(".n", "").strip()
        list_n = select_all_airplanes(select_ID_A_employee_using_id_telegram(bot.effective_user['id'])[0])
        list_n_temp = []
        if text != "":
            for item in list_n:
                if item[0].lower().find(text.lower()) != -1:
                    list_n_temp.append(item)
        else:
            list_n_temp = list_n
        for item in list_n_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[0],
                input_message_content=InputTextMessageContent(message_text=item[0]),
                thumb_url="https://previews.123rf.com/images/logos2012/logos20121509/logos2012150900042/44872922-airplane-transport-concept-2d-vector-design-on-gradient-background.jpg",
                description="Tipo: "+item[1]),
            )
            index += 1
        update.user_data['list_n'] = list_n_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".it"):
        #resultados = list()
        text = query.replace(".it", "").strip()
        list_it = select_all_type_installation_in_Supervisor()
        list_it_temp = []
        if text != "":
            for item in list_it:
                if item[0].lower().find(text.lower()) != -1:
                    list_it_temp.append(item)
        else:
            list_it_temp = list_it
        for item in list_it_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[0],
                input_message_content=InputTextMessageContent(message_text=item[0]),
                thumb_url="https://www.crushpixel.com/big-static16/preview4/duty-free-shop-front-semi-2255971.jpg",
                description=None),
            )
            index += 1
        update.user_data['list_it'] = list_it_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".i") or query.startswith(".ih"):
        #resultados = list()
        text = query.replace(".ih", "").strip() if query.startswith(".ih") else query.replace(".i", "").strip()
        list_i = select_all_installation_in_a_aeroport(select_ID_A_employee_using_id_telegram(bot.effective_user['id'])[0])
        list_i_temp = []
        if text != "":
            for item in list_i:
                if item[2].lower().find(text.lower()) != -1 or str(item[0]).find(text) != -1:
                    list_i_temp.append(item)
        else:
            list_i_temp = list_i
        for item in list_i_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[0],
                input_message_content=InputTextMessageContent(message_text=item[0]),
                thumb_url="https://www.crushpixel.com/big-static16/preview4/duty-free-shop-front-semi-2255971.jpg",
                description="Nombre: "+item[2]),
            )
            index += 1
        update.user_data['list_i'] = list_i_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".pr") or query.startswith(".prwg"):
        #resultados = list()
        if query.startswith(".prwg"):
            text = query.replace(".prwg", "").strip() 
        elif query.startswith(".prb"):
            text = query.replace(".prb", "").strip()
        elif query.startswith(".pr"):
            text = query.replace(".pr", "").strip() 
        list_pr = select_all_product_employee_inst(select_id_installation_employee(bot.effective_user['id'])[0], select_ID_A_employee_using_id_telegram(bot.effective_user['id'])[0])
        list_pr_temp = []
        if text != "":
            for item in list_pr:
                if item[1].lower().find(text.lower()) != -1:
                    list_pr_temp.append(item)
        else:
            list_pr_temp = list_pr
        for item in list_pr_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title=item[1],
                input_message_content=InputTextMessageContent(message_text=item[1]),
                thumb_url="https://thumbs.dreamstime.com/b/mail-warehouse-flat-color-vector-illustration-sending-packages-dangerous-disease-pandemic-right-to-home-delivery-company-209990473.jpg",
                description="Nombre: "+item[1]+'\n'+"Precio: "+str(item[2])+'\n'+"Cantidad: "+str(item[3])),
            )
            index += 1
        update.user_data['list_pr'] = list_pr_temp
        #update.bot.answerInlineQuery(bot.inline_query.id, results=resultados, cache_time=1)
    elif query.startswith(".rp"):
        #resultados = list()
        text = query.replace(".rp", "").strip()
        list_rp = select_repair_type()
        list_rp_temp = []
        if text != "":
            for item in list_rp:
                if item[1].lower().find(text.lower()) != -1:
                    list_rp_temp.append(item)
        else:
            list_rp_temp = list_rp

        for item in list_rp_temp: 
            resultados.append(InlineQueryResultArticle(
                id=index,
                title="Codigo: "+str(item[0]),
                input_message_content=InputTextMessageContent(message_text=item[1]),
                thumb_url="https://thumbs.dreamstime.com/b/mail-warehouse-flat-color-vector-illustration-sending-packages-dangerous-disease-pandemic-right-to-home-delivery-company-209990473.jpg",
                description="Tipo: "+item[1]+'\n'+"Precio: "+str(item[2])),
            )
            index += 1
            if index == 50:
                break
        update.user_data['list_rp'] = list_rp_temp
    update.bot.answerInlineQuery(id, results=resultados, cache_time=1)


def asd(bot, update):
    query = bot.to_dict()['chosen_inline_result']['query']
    update.bot.delete_message(chat_id=bot.effective_user['id'], message_id=update.user_data['message_id'])
    if query.startswith(".pc") or query.startswith(".phr") or query.startswith(".pp") or query.startswith(".po"):        
        if query.startswith(".pc"):
            update.user_data['country'] = update.user_data['list_countries'][int(bot.to_dict()['chosen_inline_result']['result_id'])]
            msg = client_registration_refresh_menu(bot.effective_user['first_name'], update)
        elif query.startswith(".phr"):
            update.user_data['country'] = update.user_data['list_countries'][int(bot.to_dict()['chosen_inline_result']['result_id'])]
            msg = employee_add_refresh_menu(update)
        elif query.startswith(".pp"):
            update.user_data['passeger_country'] = update.user_data['list_countries'][int(bot.to_dict()['chosen_inline_result']['result_id'])]
            msg = into_data_pasajero_refresh_client_menu(update)
        elif query.startswith(".po"):
            update.user_data['owner_country'] = update.user_data['list_countries'][int(bot.to_dict()['chosen_inline_result']['result_id'])]
            msg = into_data_owner_refresh_client_menu(update) 
    elif query.startswith(".fs") or query.startswith(".fsgv"):
        update.user_data["fecha"] = update.user_data['list_date_go'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        if query.startswith(".fs"):
            msg = make_prebooking_client_refresh_menu(update)
        elif query.startswith(".fsgv"):
            msg = make_prebooking_salesManager_refresh_menu(update)
    elif query.startswith(".ld") or query.startswith(".ldgv"):
        update.user_data["destino"] = update.user_data['list_dest'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        if query.startswith(".ld"):
            msg = make_prebooking_client_refresh_menu(update)
        elif query.startswith(".ldgv"):
            msg = make_prebooking_salesManager_refresh_menu(update)
    elif query.startswith(".lo") or query.startswith(".logv"):
        update.user_data["origen"] = update.user_data['list_orig'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        if query.startswith(".lo"):
            msg = make_prebooking_client_refresh_menu(update)
        elif query.startswith(".logv"):
            msg = make_prebooking_salesManager_refresh_menu(update)
    elif query.startswith(".a") or query.startswith(".agv"):
        update.user_data["aerolinea"] = update.user_data['list_aerol'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        if query.startswith(".a"):
            msg = make_prebooking_client_refresh_menu(update)
        elif query.startswith(".agv"):
            msg = make_prebooking_salesManager_refresh_menu(update)
    elif query.startswith(".vm"): 
        update.user_data["vuelo"] = update.user_data['list_vuelos'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        msg = employee_counter_menu2(update.effective_user['first_name'])
    elif query.startswith(".cm"): 
        update.user_data["ID_C"] = update.user_data['list_cm'][int(bot.to_dict()['chosen_inline_result']['result_id'])][4]
        update.user_data["info"] = select_client_data_and_his_flight(update.user_data["ID_F"], update.user_data["ID_C"])[0]
        msg = employee_counter_menu3(update.user_data["info"])
    elif query.startswith(".nfl"): 
        msg = employee_flightOperator_flight_selected(update.user_data['list_nave'][int(bot.to_dict()['chosen_inline_result']['result_id'])])
    elif query.startswith(".ne") or query.startswith(".ns"):
        msg = employee_flightOperator_prog_flight_selected(update.user_data['list_nave'][int(bot.to_dict()['chosen_inline_result']['result_id'])])
    elif query.startswith(".ved"):
        update.user_data["id_vuelo"] = update.user_data['list_vuelo'][int(bot.to_dict()['chosen_inline_result']['result_id'])][6]
        msg = employee_exitDoor_passenger_list_menu()
    elif query.startswith(".ce") or query.startswith(".cs"):
        update.user_data["type_c"] = "ce" if query.startswith(".ce") else "cs"
        update.user_data["ID_C"] =  update.user_data['list_c'][int(bot.to_dict()['chosen_inline_result']['result_id'])][4]
        update.user_data["ID_F"] =  update.user_data['list_c'][int(bot.to_dict()['chosen_inline_result']['result_id'])][5]
        msg = employee_immigration_passenger_menu(update.user_data['list_c'][int(bot.to_dict()['chosen_inline_result']['result_id'])])
    elif query.startswith(".cp"):
        update.user_data["ID_Prereserva"] =  update.user_data['list_cp'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        msg = modif_all_options_menu()
    elif query.startswith(".cod"):
        update.user_data["ID_Prereserva"] =  update.user_data['list_cod'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        item = select_Booking(update.user_data["ID_Prereserva"])[0]
        msg = employee_salesManager_prereserva_view_menu(item)
    elif query.startswith(".c"):
        update.user_data['job'] = update.user_data['list_jobs'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        msg = employee_add_refresh_menu(update)
    elif query.startswith(".v"):
        update.user_data["ID_F"] =  update.user_data['list_v'][int(bot.to_dict()['chosen_inline_result']['result_id'])][6]
        msg = employee_counter_menu2()
    elif query.startswith(".e"):
        update.user_data['del_employee'] = update.user_data['list_employees'][int(bot.to_dict()['chosen_inline_result']['result_id'])]
        msg = employee_humanResources_info_menu(update.user_data['del_employee'])
    elif query.startswith(".i"):
        if query.startswith(".it"):
            update.user_data["tipo_inst"] = update.user_data['list_it'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
            msg = employee_facilitiesSupervisor_add_refresh_menu(update)
        elif query.startswith(".ih"):
            update.user_data['ID_I'] = update.user_data['list_i'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
            msg = employee_add_refresh_menu(update)
        else:
            update.user_data['ID_I'] = update.user_data['list_i'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
            msg = select_installation_info(update.user_data['ID_I'], select_ID_A_employee_using_id_telegram(bot.effective_user['id'])[0])[0]
            msg = employee_facilitiesSupervisor_refresh_menu(msg)
    elif query.startswith(".pr"):
        if query.startswith(".prb"):
            update.user_data['codigo_prod'] = update.user_data['list_pr'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
            msg = employee_installation_purchases_refresh_menu(update)
        else:
            update.user_data['ID_P'] = update.user_data['list_pr'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
            msg = employee_installation_wareHouse_info_prod_menu(select_product(update.user_data['ID_P'])[0])
    elif query.startswith(".np"):
        update.user_data['No_P'] = update.user_data['list_np'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        msg = pasaje_futuro_menu()
    elif query.startswith(".n"):
        update.user_data['enrollment'] = update.user_data['list_n'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        repair = select_airplane_repairs(update.user_data['enrollment'], select_ID_A_employee_using_id_telegram(bot.effective_user['id'])[0], select_id_installation_employee(bot.effective_user['id'])[0])
        msg=employee_chiefMachanic_refresh_menu(repair[0][0], repair[1])
    elif query.startswith(".prwg"):
        update.user_data['ID_P'] = update.user_data['list_pr'][int(bot.to_dict()['chosen_inline_result']['result_id'])][0]
        msg = employee_installation_wareHouse_info_prod_menu(select_product(update.user_data['ID_P'])[0])
    elif query.startswith(".rp"):
        update.user_data['repair'] = update.user_data['list_rp'][int(bot.to_dict()['chosen_inline_result']['result_id'])]
        msg = employee_chiefMachanic_add_repair_refresh_menu(update)
    update.user_data['message_id'] = update.bot.send_message(chat_id=bot.effective_user['id'], text=msg[0], parse_mode='Markdown', reply_markup=msg[1]).message_id

def main():
    TOKEN = os.environ.get("TOKEN")
    update = Updater(TOKEN, use_context=True)
    dp = update.dispatcher

    start_handler = ConversationHandler(
        entry_points = [
            CommandHandler('start', start), 
        ],
        states = {
            START: [CallbackQueryHandler(start_callback_query)],
            CLIENT_REGISTRATION: [CallbackQueryHandler(client_registration_callback_query, pass_user_data=True)], 
            NAME_CLIENT: [MessageHandler(Filters.text, name_client_callback_query, pass_user_data=True)],
            LAST_NAME_CLIENT: [MessageHandler(Filters.text, last_name_client_callback_query, pass_user_data=True)],
            COUNTRY_CLIENT: [MessageHandler(Filters.text, country_client_callback_query, pass_user_data=True)],
            No_Passport_CLIENT: [MessageHandler(Filters.text, no_passport_client_callback_query, pass_user_data=True)],
            SAVE_DATA_CLIENT: [CallbackQueryHandler(save_data_client_callback_query, pass_user_data=True)], 
            CLIENT_OPTIONS: [CallbackQueryHandler(client_options_callback_query, pass_user_data=True)],
            CLIENT_PREBOOKING : [CallbackQueryHandler(client_prebooking_callback_query, pass_user_data=True)],
            CLIENT_MAKE_PREBOOKING: [CallbackQueryHandler(client_make_prebooking_callback_query, pass_user_data=True)],
            CLIENT_CANT_PASAJES: [MessageHandler(Filters.text, client_cant_pasajeros_message_text, pass_user_data=True)],

            SAVE_PREBOOKING_CLIENT: [CallbackQueryHandler(save_prebooking_client_callback_query, pass_user_data=True)],
            CLIENT_INTO_DATA_PASS: [CallbackQueryHandler(prebooking_data_passenger_client_callback_query, pass_user_data=True)],
            NAME_PASSEGER: [MessageHandler(Filters.text, name_passeger_message_text, pass_user_data=True)],
            LAST_NAME_PASSEGER: [MessageHandler(Filters.text, last_name_passeger_message_text, pass_user_data=True)],
            No_Passport_PASSEGER: [MessageHandler(Filters.text, no_passport_passeger_message_text, pass_user_data=True)],
            CLIENT_SAVE_DATA_PASS: [CallbackQueryHandler(save_passeger_client_callback_query, pass_user_data=True)],

            NEW_EMPLOYEE_OPTIONS_CQ: [CallbackQueryHandler(new_employee_options_callback_query, pass_user_data=True)],
            NEW_EMPLOYEE: [MessageHandler(Filters.text, new_employee_verification_code_message_text, pass_user_data=True)],
            EMPLOYEE_HUMAN_RESOURCES: [CallbackQueryHandler(employee_human_resources_options_callback_query, pass_user_data=True)],
            EMPLOYEE_LIST: [CallbackQueryHandler(employee_list_callback_query, pass_user_data=True)],
            EMPLOYEE_ADD: [CallbackQueryHandler(employee_add_callback_query, pass_user_data=True)],
            EMPLOYEE_DNI: [MessageHandler(Filters.text, dni_employee_message_text, pass_user_data=True)], 
            EMPLOYEE_NAME: [MessageHandler(Filters.text, name_employee_message_text, pass_user_data=True)],
            EMPLOYEE_LAST_NAME: [MessageHandler(Filters.text, last_name_employee_message_text, pass_user_data=True)],

            EMPLOYEE_IMMIGRATION: [CallbackQueryHandler(employee_immigration_options_callback_query)],

            EMPLOYEE_FACILITIESSUPERVISOR: [CallbackQueryHandler(employee_facilitiesSupervisior)],
            EMPLOYEE_FACILITIESSUPERVISOR_ADD: [CallbackQueryHandler(employee_facilitiesSupervisior_add_inst)],
            EMPLOYEE_FACILITIESSUPERVISOR_INST_NAME: [MessageHandler(Filters.text, employee_facilitiesSupervisior_inst_name_message_text)],

            EMPLOYEE_WAREHOUSEMANGER_ADD_PROD: [CallbackQueryHandler(employee_warehouseManager_addProd_callback_query)],
            EMPLOYEE_WAREHOUSEMANGER_NAME_PROD: [MessageHandler(Filters.text, employee_warehouseManager_nameProd_message_text)],
            EMPLOYEE_WAREHOUSEMANGER_CANT: [MessageHandler(Filters.text, employee_warehouseManager_cant_message_text)],
            EMPLOYEE_WAREHOUSEMANGER_PRICE: [MessageHandler(Filters.text, employee_warehouseManager_price_message_text)],
            EMPLOYEE_WAREHOUSEMANGER: [CallbackQueryHandler(employee_warehouseManager_callback_query)],

            EMPLOYEE_EXITDOOR: [CallbackQueryHandler(employee_exitDoor_callback_query)],
            EMPLOYEE_EXITDOOR_COMPL_LIST: [CallbackQueryHandler(employee_exitDoor_complete_List_callback_query)],
            EMPLOYEE_EXITDOOR_CLINT_TO_CLIENT: [CallbackQueryHandler(employee_exitDoor_client_to_client_callback_query)],

            EMPLOYEE_FLIGHTOPERATOR: [CallbackQueryHandler(employee_flightOperator_callback_query)],
            EMPLOYEE_FLIGHTOPERATOR_PROG: [CallbackQueryHandler(employee_flightOperator_prog_callback_query)],

            EMPLOYEE_CHIEFMACHANIC: [CallbackQueryHandler(employee_chiefMachanic_callback_query)],
            EMPLOYEE_CHIEFMACHANIC_ADD_NAVE: [CallbackQueryHandler(employee_chiefMachanic_add_nave_callback_query)],
            EMPLOYEE_CHIEFMACHANIC_ADD_REPAIR: [CallbackQueryHandler(employee_chiefMachanic_add_repair_callback_query)],
            EMPLOYEE_CHIEFMACHANIC_MATRICULA: [MessageHandler(Filters.text, employee_chiefMachanic_matricula_message_text)],
            EMPLOYEE_CHIEFMACHANIC_CAPACITY: [MessageHandler(Filters.text, employee_chiefMachanic_capacidad_message_text)],
            EMPLOYEE_CHIEFMACHANIC_TIPO: [MessageHandler(Filters.text, employee_chiefMachanic_tipo_message_text)],
            EMPLOYEE_CHIEFMACHANIC_DURACION: [MessageHandler(Filters.text, employee_chiefMachanic_duracion_message_text)],

            EMPLOYEE_INSTALLATION: [CallbackQueryHandler(employee_installation_callback_query)],
            EMPLOYEE_INSTALLATION_PURCHASES: [CallbackQueryHandler(employee_installation_purchases_callback_query)],
            EMPLOYEE_INSTALLATION_WAREHOUSE: [CallbackQueryHandler(employee_installation_warehouse_callback_query)],
            EMPLOYEE_INSTALLATION_PURCHASES_CODE_PROD: [MessageHandler(Filters.text, employee_installation_purchases_code_prod_message_text)],
            EMPLOYEE_INSTALLATION_PURCHASES_CANT: [MessageHandler(Filters.text, employee_installation_purchases_cant_message_text)],

            EMPLOYEE_SALESMANAGER: [CallbackQueryHandler(employee_salesManager_callback_query)],
            EMPLOYEE_SALESMANAGER_PASAJE: [CallbackQueryHandler(employee_salesManager_pasajes_callback_query)],
            EMPLOYEE_SALESMANAGER_PRERESERVA: [CallbackQueryHandler(employee_salesManager_prereserva_callback_query)],
            EMPLOYEE_SALESMANAGER_SELLPASAJE: [CallbackQueryHandler(employee_salesManager_sellpasaje_data_callback_query)],
            EMPLOYEE_SALESMANAGER_CANT_PASAJEROS: [MessageHandler(Filters.text, employee_salesManager_cantPasajes_message_text)],
            EMPLOYEE_SALESMANAGER_MODIFPASAJE: [CallbackQueryHandler(employee_salesmanager_modifpasaje_callback_query)],
            EMPLOYEE_SALESMANAGER_INTO_DATA_PASS: [CallbackQueryHandler(into_data_passeger_salesManager_callback_query)],
            EMPLOYEE_SALESMANAGER_PRERESERVA_DETAILS: [CallbackQueryHandler(save_passeger_salesManager_callback_query)],
            EMPLOYEE_SALESMANAGER_PRERESERVA_CODE: [CallbackQueryHandler(employee_salesManager_prereserva_code)], 
            SAVE_PREBOOKING_SALESMANAGER: [CallbackQueryHandler(save_data_salesManager_callback_query)], 

            NAME_PASSEGER_SALESMANAGER: [MessageHandler(Filters.text, name_passeger_salesManager_message_text)],
            LAST_NAME_PASSEGER_SALESMANAGER: [MessageHandler(Filters.text, last_name_passeger_salesManager_message_text)],
            No_Passport_PASSEGER_SALESMANAGER: [MessageHandler(Filters.text, no_passport_passeger_salesManager_message_text)],
            SAVE_OWNER_PREBOOKING_SALESMANAGER: [CallbackQueryHandler(save_data_owner_booking)],
            EMPLOYEE_SALESMANAGER_INTO_DATA_OWNER: [CallbackQueryHandler(into_data_owner_salesManager_callback_query)],
            NAME_OWNER_SALESMANAGER: [MessageHandler(Filters.text, name_owner_salesManager_message_text)],
            LAST_NAME_OWNER_SALESMANAGER: [MessageHandler(Filters.text, last_name_owner_salesManager_message_text)],
            No_Passport_OWNER_SALESMANAGER: [MessageHandler(Filters.text, no_passport_owner_salesManager_message_text)],

            EMPLOYEE_COUNTER: [CallbackQueryHandler(employee_counter_callback_query)],
            EMPLOYEE_COUNTER_MT: [MessageHandler(Filters.text, employee_counter_cantMaletas_message_text)],
		}, 
        fallbacks = []
    )

    dp.add_handler(start_handler)
    dp.add_handler(InlineQueryHandler(inline, pass_user_data=True))
    dp.add_handler(ChosenInlineResultHandler(asd, pass_user_data=True))

    #create_tables()
    #insert_all_data()

    run(update)

if __name__ == "__main__":
    main()
