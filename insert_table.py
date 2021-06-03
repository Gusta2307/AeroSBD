import psycopg2
import os
from datetime import *  

from contains import *
from update_table import *
from select_from_table import *

DATABASE_URL = os.environ.get("DATABASE_URL")

def insert_vendor(vendor_name):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (vendor_name,))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_client(update, context):
    name = context.user_data["name"]
    last_name = context.user_data["last_name"]
    country = context.user_data["country"]
    id_telegram = update._effective_chat['id']
    no_passport = context.user_data["no_passport"]

    print("INSERT CLIENT")    
    print(name)
    print(last_name)
    print(country)
    print(id_telegram)
    print(no_passport)

    is_client = contains_client(str(no_passport))
    if is_client != []:
        if is_client[0][1] != None:
            id_telegram_client_update(is_client[0][0], id_telegram)
        return

    query = """INSERT INTO Client (Name_C, Last_name_C, Country_C, ID_Telegram_C, No_Passport) 
            VALUES (%s,%s,%s,%s,%s);
        """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (name,last_name,country,id_telegram, no_passport))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()  

def insert_client_booking(data):
    is_client = contains_client(data[3])
    if is_client == []:
        query = """INSERT INTO Client (Name_C, Last_name_C, Country_C, ID_Telegram_C, No_Passport) 
                VALUES (%s,%s,%s,%s,%s);
            """
        conn = None
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()
            cur.execute(query, (data[0], data[1], data[2], None, data[3]))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    print("SALI INSERT CLIENT")

def insert_employee(update, context):
    name = context.user_data["name_employee"]
    last_name = context.user_data["last_name_employee"]
    country = context.user_data["country"]
    verification_code = context.user_data["verif_code"]
    #id_telegram = update._effective_chat.id
    job = context.user_data["job"]
    dni = context.user_data["dni_employee"]
    id_i = context.user_data["ID_I"]

    query = """INSERT INTO Employee (Name_E, Last_name_E, Country_NE, Cod_Verif, Job, DNI, ID_AeroP, ID_I) 
            VALUES (%s,%s,%s,%s,%s,%s, %s, %s)
        """
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        ID_AeroP = select_ID_A_employee_using_id_telegram(update._effective_chat['id'])
        cur.execute(query, (name, last_name, country, verification_code, job, dni, ID_AeroP, id_i))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# registrar los datos del vuelo
def insert_flight_datas(cod_F, id_A, enrollment, loc_O, aero_S, fh_S, loc_D, aero_L, fh_L):
    
    query = f"""INSERT INTO Flight (cod_F, ID_A, Enrollment, Lugar_Origen, Aeropuerto_S, 
                                    Fecha_Hora_S, Lugar_Destino, Aeropuerto_L, Fecha_Hora_L) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (cod_F, id_A, enrollment, loc_O, aero_S, fh_S, loc_D, aero_L, fh_L))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# registrar los datos de la prereserva
def insert_booking_datas(id_C, id_F, client_list):
    print("INSERT")
    print("id_C")
    print(id_C)
    print("id_F")
    print(id_F)
    print("client_list")
    print(client_list)
    query1 = """INSERT INTO Booking (ID_C, ID_F, Date_booking, IS_paid) 
            VALUES (%s, %s, CURRENT_TIMESTAMP, 0);
        """
    query2 = """INSERT INTO BookingTo (ID_B, ID_C) 
            VALUES (%s, %s);
        """
    conn = None 
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query1, (id_C, id_F))
        ID_B = select_the_last_booking()
        for client in client_list:
            id_c = select_ID_client_using_no_passport(client)
            cur.execute(query2, (ID_B[0][0], id_c[0][0]))

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    print("SALIO INSERT BOOKING")

# registrar reparacion a una nave
def insert_nave_repair(cod_R, enrollment, tipo_R):
    query = f"""INSERT INTO Repair (Cod_R, Enrollment, Tipo_R) 
            VALUES (%s,%s,%s);
        """

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (cod_R, enrollment, tipo_R))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# registrar pasaje
def insert_passage(cod_F, id_C, seat):

    query = f"""INSERT INTO Airfare (cod_F, ID_CR) 
            VALUES (%s,%s);
        """

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (cod_F, id_C))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# registrar reserva
def insert_booking(cod_F, id_C, id_CR, fecha_R):
    query = """INSERT INTO Booking (cod_F, ID_C, ID_CR, Fecha_R) 
            VALUES (%s,%s,%s,%s);
        """
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (cod_F, id_C, id_CR, fecha_R))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#INSERTAR en flujo de pasajeros
def insert_passenger_in_Passenger_Flow(ID_C, ID_F, isAccepted_S):
    query = """INSERT INTO Passenger_Flow(ID_C, ID_F, isAccepted_S) 
            VALUES(%s, %s, %s)
        """
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (ID_C, ID_F, isAccepted_S))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_apply_repair_repair(Enrollment, Cod_R, Days, ID_AeroP, ID_I):
    # fecha actual
    now = str(datetime.now()).split('.')[0]
    query1 = f"""
            INSERT INTO date (Date_Begin)
            SELECT timestamp {now} WHERE NOT EXISTS (SELECT Date_Begin FROM Date);
    """
    begin = str(datetime.now() + timedelta(days=-int(Days))).split('.')
    query = f"""INSERT INTO Apply_Repair(Enrollment, Cod_R, Date_Begin, Date_End, Time, ID_AeroP, ID_I) 
               VALUES(%s, %s, timestamp {begin}, timestamp {now}, %s, %s, %s)
            """

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query1,)
        conn.commit()
        print("MMMMMMMM")
        cur.execute(query, (Enrollment, Cod_R, 0, ID_AeroP, ID_I))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_installation(ID_AeroP, Name_I, Type):
    query = """INSERT INTO Installation(ID_AeroP, Name_I, Type) 
            VALUES(%s, %s, %s)
        """
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (ID_AeroP, Name_I, Type))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    

def insert_product(name, cost, count, ID_AeroP, ID_I):
    query = """INSERT INTO Product(Name_Prod, Cost_Prod) 
            VALUES(%s, %s)
            """
    query1 = """INSERT INTO Product_Installation(ID_AeroP, ID_I, ID_Prod, Count_Prod)
            VALUES(%s, %s, %s, %s)
            """
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (name, cost))
        conn.commit()
        id_p = select_the_last_product()[0][0]
        cur.execute(query1, (ID_AeroP, ID_I, id_p, count))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    

def insert_airplane(Enrollment, Clasif, Capacity):
    query = """INSERT INTO Airplane(Enrollment, Clasif, Capacity) 
               VALUES(%s, %s, %s)
            """

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, (Enrollment, Clasif, Capacity))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_buy(ID_Prod, Count_Prod, ID_I, ID_AeroP, cant_exits):
    query = """INSERT INTO Buy(Date_Buy) 
            VALUES(CURRENT_TIMESTAMP)
            """
    query1 = """INSERT INTO Product_Buy(ID_Prod, ID_Buy, Count_Prod, ID_I, ID_AeroP)
            VALUES(%s, %s, %s, %s, %s)
            """
    
    query2 = \
        """
            UPDATE Product_Installation SET Count_Prod = %s WHERE ID_AeroP = %s AND ID_I = %s AND ID_Prod = %s
        """

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query, )
        ID_Buy = select_the_last_buy()[0][0]
        cur.execute(query1, (ID_Prod, ID_Buy, Count_Prod, ID_I, ID_AeroP))
        cur.execute(query2, (str(cant_exits - int(Count_Prod)), ID_AeroP, ID_I, ID_Prod))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()