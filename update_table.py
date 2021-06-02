import psycopg2
import os
from select_from_table import *

DATABASE_URL = os.environ.get("DATABASE_URL")


def id_telegram_employee_update(id_T, id_E):
    command = (
        f""" 
        UPDATE Employee SET ID_Telegram_E = \'{id_T}\', Cod_Verif = \'\' WHERE ID_E = {id_E}
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
            
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def id_telegram_client_update(ID_C, id_telegram):
    command = (
        f""" 
        UPDATE Client SET ID_Telegram_C = {id_telegram} WHERE ID_C = {ID_C}
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
            
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
#FLUJO DE PASAJEROS, cambiar nombre
def passengers_on_update(ID_C, ID_F, isAccepted_E):
    command = (
        f""" 
        UPDATE Passenger_Flow SET isAccepted_E = {isAccepted_E} WHERE ID_C = {ID_C} AND ID_F = {ID_F} AND isAccepted_S = \'1\'
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
            
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def airfare_update(ID_C, ID_F, count):
    command = (
        f""" 
        UPDATE Airfare SET Count_Baggage = {count} WHERE ID_C = {ID_C} AND ID_F = {ID_F}
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
            
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def product_update(ID_Prod, Name_Prod, Cost_Prod, Count_Prod):
    command = (
        f""" 
        UPDATE Product SET ID_Prod = {ID_Prod}, Name_Prod = {Name_Prod}, Cost_Prod = {Cost_Prod}, Count_Prod = {Count_Prod} WHERE ID_Prod = {ID_Prod}
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def buy_product_update(id_AeroP, id_I, id_Prod):
    cant_product = select_cant_product_inst(id_AeroP, id_I, id_Prod)[0][0]
    command = (
        f""" 
        UPDATE Product_Installation 
        SET Product_Installation.Count_Prod = Product_Installation.Count_Prod - Product_Buy.Count_Prod
        WHERE ID_AeroP = \'{id_AeroP}\' AND ID_I = \'{id_I}\' ID_Prod = \'{id_Prod}\'
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def booking_is_paid_update(ID_B):
    command = (
        f""" 
        UPDATE Booking SET IS_paid = \'1\' WHERE ID_B = \'{ID_B}\'
        """,)
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_booking(orig, dest, aero, fecha, ID_B):
    command = "UPDATE Booking SET "
    # IS_paid = \'1\' WHERE ID_B = \'{ID_B}\'"""
    #if oring != "":

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        # close communication with the PostgreSQL database server
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

