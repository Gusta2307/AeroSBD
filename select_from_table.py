import psycopg2
import os 

#import date

DATABASE_URL = os.environ.get("DATABASE_URL")

#Cliente: Filtrado de fechas
def select_date_go(context):
    query = "SELECT Date_Hour_S FROM Flight "
    #isEmply = select_all_booking()

    if context.user_data['cant_pasajes'] != "":# and not isEmply:
        command1 = f"SELECT ID_F FROM (SELECT ID_F, Total_Passenger FROM Flight INNER JOIN Flight_Matric USING(ID_F) INNER JOIN Airplane USING(Enrollment) INNER JOIN Total_Passenger USING(Clasif, Capacity, No_Tripulante)) AS Total INNER JOIN (SELECT ID_F, Count(*) as asientos FROM Booking GROUP BY ID_F) AS total_asientos  USING(ID_F) WHERE Total_Passenger - asientos >= {context.user_data['cant_pasajes']} "
        query += "INNER JOIN (" + command1 + ") AS cant_pasajeros USING(id_F) "

    if context.user_data['origen'] != "":
        command2 = f"SELECT ID_F FROM Flight WHERE Aeroport_S = {context.user_data['origen']} "
        query += "INNER JOIN (" + command2 + ") AS origen USING(ID_F) "

    if context.user_data['destino'] != "":
        command3 = f"SELECT ID_F FROM Flight WHERE Aeroport_L = {context.user_data['destino']} "
        query += "INNER JOIN (" + command3 + ") AS destino USING(ID_F) "

    if context.user_data['aerolinea'] != "":
        command4 = f"SELECT ID_F FROM Flight  WHERE ID_A = {context.user_data['aerolinea']} "
        query += "INNER JOIN (" + command4 + ") AS a USING(ID_F) "


    query+= "WHERE Date_Hour_S > CURRENT_DATE + INTERVAL '1 hr' GROUP BY Date_Hour_S"

    command = (query, )
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

#Cliente: Filtrado para cantidad de pasajeros
def select_passengers_count(context, count):
    query = f"SELECT ID_F FROM (SELECT ID_F, Total_Passenger FROM (SELECT ID_F FROM Flight WHERE Date_Hour_S > CURRENT_DATE + INTERVAL '1 hr')AS fechaS INNER JOIN Flight_Matric USING(ID_F) INNER JOIN Airplane USING(Enrollment) INNER JOIN Total_Passenger USING(Clasif, Capacity, No_Tripulante)) AS Total INNER JOIN (SELECT ID_F, Count(*) as asientos FROM Booking GROUP BY ID_F) AS total_asientos  USING(ID_F)  "
    
    if context.user_data['origen'] != "":
        command2 = f"SELECT ID_F FROM Flight WHERE Flight.Aeroport_S = {context.user_data['origen']} "
        query += "INNER JOIN (" + command2 + ") AS origen USING(ID_F) "
    if context.user_data['destino'] != "":
        command3 = f"SELECT ID_F FROM Flight WHERE Flight.Aeroport_L = {context.user_data['destino']} "
        query += "INNER JOIN (" + command3 + ") AS destino USING(ID_F) "
    if context.user_data['aerolinea'] != "":
        command4 = f"SELECT ID_F FROM Flight  WHERE Flight.ID_A = {context.user_data['aerolinea']} "
        query += "INNER JOIN (" + command4 + ") AS a USING(ID_F) "
    if context.user_data['fecha'] != "":
        command5 = f"SELECT ID_F FROM Flight WHERE Flight.Date_Hour_S = \'{context.user_data['fecha']}\' "
        query += "INNER JOIN (" + command5 + ") AS fecha USING(ID_F) "

    query += f"WHERE Total_Passenger - asientos > 0 "

    command = (query, )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result 

#Cliente: Filtrado para el lugar de origen 
def select_airport_source(context):
    query = "SELECT ID_AeroP, Name_AeroP, Pos_Geog, Direction FROM Flight INNER JOIN Aeroport ON Flight.Aeroport_S = Aeroport.ID_AeroP "

    if context.user_data['cant_pasajes'] != "":
        
        command1 = f"SELECT ID_F, Total_Passenger FROM Flight INNER JOIN Flight_Matric USING(ID_F) INNER JOIN Airplane USING(Enrollment) INNER JOIN Total_Passenger USING(Clasif, Capacity, No_Tripulante) INNER JOIN (SELECT ID_F, Count(*) as asientos FROM Booking GROUP BY ID_F) AS total_asientos  USING(ID_F) WHERE Total_Passenger - asientos >= {context.user_data['cant_pasajes']}"
        query += "INNER JOIN (" + command1 + ")  AS cant_pasajeros USING(id_F) "

    if context.user_data['fecha'] != "":
        command5 = f"SELECT ID_F FROM Flight WHERE Flight.Date_Hour_S = \'{context.user_data['fecha']}\' "
        query += "INNER JOIN (" + command5 + ") AS fecha USING(ID_F) "

    if context.user_data['destino'] != "":
        command3 = f"SELECT ID_F FROM Flight WHERE Flight.Aeroport_L = {context.user_data['destino']} "
        query += "INNER JOIN (" + command3 + ") AS destino USING(ID_F) "

    if context.user_data['aerolinea'] != "":
        command4 = f"SELECT ID_F FROM Flight  WHERE Flight.ID_A = {context.user_data['aerolinea']} "
        query += "INNER JOIN (" + command4 + ") AS a USING(ID_F) "

    query+= "WHERE Date_Hour_S > CURRENT_DATE + INTERVAL '7 hr' GROUP BY ID_AeroP"

    command = (query, )
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

#Cliente: Filtrado para el lugar de destino 
def select_airport_destination(context):
    query = "SELECT ID_AeroP, Name_AeroP, Pos_Geog, Direction FROM Flight INNER JOIN Aeroport ON Flight.Aeroport_L = Aeroport.ID_AeroP "

    if context.user_data['cant_pasajes'] != "":
        command1 = f"SELECT ID_F FROM (SELECT ID_F, Total_Passenger FROM Flight INNER JOIN Flight_Matric USING(ID_F) INNER JOIN Airplane USING(Enrollment) INNER JOIN Total_Passenger USING(Clasif, Capacity, No_Tripulante)) AS Total INNER JOIN (SELECT ID_F, Count(*) as asientos FROM Booking GROUP BY ID_F) AS total_asientos  USING(ID_F) WHERE Total_Passenger - asientos >= {context.user_data['cant_pasajes']} "
        query += "INNER JOIN (" + command1 + ") AS cant_pasajeros USING(id_F) "

    if context.user_data['fecha'] != "":
        command5 = f"SELECT ID_F FROM Flight WHERE Flight.Date_Hour_S = \'{context.user_data['fecha']}\' "
        query += "INNER JOIN (" + command5 + ") AS fecha USING(ID_F) "


    if context.user_data['origen'] != "":
        command2 = f"SELECT ID_F FROM Flight WHERE Flight.Aeroport_S = {context.user_data['origen']} "
        query += "INNER JOIN (" + command2 + ") AS origen USING(ID_F) "


    if context.user_data['aerolinea'] != "":
        command4 = f"SELECT ID_F FROM Flight  WHERE Flight.ID_A = {context.user_data['aerolinea']} "
        query += "INNER JOIN (" + command4 + ") AS a USING(ID_F) "

    query+= "WHERE Date_Hour_S > CURRENT_DATE + INTERVAL '7 hr' GROUP BY ID_AeroP"

    command = (query, )
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

#Cliente: Filtrado para la aerolinea
def select_Aeroline(context):
    query = "SELECT ID_A, Name_A, Country_NA FROM Flight INNER JOIN Aeroline USING(ID_A) "

    if context.user_data['cant_pasajes'] != "":
        command1 = f"SELECT ID_F FROM (SELECT ID_F, Total_Passenger FROM Flight INNER JOIN Flight_Matric USING(ID_F) INNER JOIN Airplane USING(Enrollment) INNER JOIN Total_Passenger USING(Clasif, Capacity, No_Tripulante)) AS Total INNER JOIN (SELECT ID_F, Count(*) as asientos FROM Booking GROUP BY ID_F) AS total_asientos  USING(ID_F) WHERE Total_Passenger - asientos > {context.user_data['cant_pasajes']} "
        query += "INNER JOIN (" + command1 + ")  AS cant_pasajeros USING(id_F) "

    if context.user_data['fecha'] != "":
        command5 = f"SELECT ID_F FROM Flight WHERE Flight.Date_Hour_S = \'{context.user_data['fecha']}\' "
        query += "INNER JOIN (" + command5 + ") AS fecha USING(ID_F) "

    if context.user_data['origen'] != "":
        command2 = f"SELECT ID_F FROM Flight WHERE Flight.Aeroport_S = {context.user_data['origen']} "
        query += "INNER JOIN (" + command2 + ") AS origen USING(ID_F) "

    if context.user_data['destino'] != "":
        command3 = f"SELECT ID_F FROM Flight WHERE Flight.Aeroport_L = {context.user_data['destino']} "
        query += "INNER JOIN (" + command3 + ") AS destino USING(ID_F) "

    query+= "WHERE Date_Hour_S > CURRENT_DATE + INTERVAL '7 hr' GROUP BY (ID_A, Name_A, Country_NA)"

    command = (query, )
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result
 
#Cliente: Obtener ID_P de la ultima prereserva hecha 
def select_the_last_booking():
    command = (
        f""" 
        SELECT ID_B FROM Booking ORDER BY ID_B DESC LIMIT 1
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

# Cliente: Ver prereservas
def select_client_booking(id_T):
    print(id_T)
    command = (
        f"""
        SELECT ID_B, Date_booking, Cod_F, Name_A, COUNT(ID_B), Aero_S, Aero_L, Date_Hour_S, Date_Hour_L, Price
        FROM (SELECT ID_B, Date_booking, Cod_F, Name_A, Aero_S, Aero_L, Date_Hour_S, Date_Hour_L, Price
                    FROM(SELECT ID_B, Date_booking, Cod_F, ID_A, Aero_S, Name_AeroP as Aero_L, Date_Hour_S, Aeroport_L, Date_Hour_L, Price
                         FROM (SELECT ID_B, Date_booking, Cod_F, ID_A , Name_AeroP as Aero_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price
                               FROM(SELECT IS_paid, ID_B, Date_booking, Cod_F, ID_A , Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price
                                    FROM(SELECT ID_B, ID_F, Date_booking, IS_paid
                                         FROM Client INNER JOIN Booking USING(ID_C)
                                         WHERE ID_Telegram_C = \'{id_T}\'
                                        ) as P1 INNER JOIN Flight USING(ID_F)
                                    WHERE IS_paid = \'0\'
                                    ) as P2
                                    INNER JOIN Aeroport ON Aeroport_S = Aeroport.ID_AeroP
                               ) as P3
                               INNER JOIN Aeroport ON Aeroport_L = Aeroport.ID_AeroP
                        ) as P4
                        INNER JOIN Aeroline USING(ID_A)
              ) as P5 INNER JOIN BookingTo USING(ID_B)
        GROUP BY ID_B, Date_booking, Cod_F, Name_A, Aero_S, Aero_L, Date_Hour_S, Date_Hour_L, Price
        ORDER BY Date_booking
        """,)

    conn = None
    result1 = None  

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result1

# Cliente: Ver vuelos futuros
def select_client_future_flight(id_T):
    command = (
        f"""
        SELECT Cod_F, Name_A, Aero_S, Date_Hour_S, Aero_L, Date_Hour_L, Price 
        FROM(SELECT Cod_F, ID_A, Aero_S, Date_Hour_S, Name_AeroP as Aero_L, Date_Hour_L, Price 
             FROM(SELECT Cod_F, ID_A, Name_AeroP as Aero_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price 
                  FROM(SELECT Cod_F, ID_A, Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price 
                       FROM(SELECT *
                            FROM Client INNER JOIN Airfare USING(ID_C)
                            WHERE ID_Telegram_C = \'{id_T}\'
                            ) as P1
                            INNER JOIN Flight USING(ID_F)
                      ) as P2
                      INNER JOIN Aeroport ON Aeroport_S = Aeroport.ID_AeroP
                  ) as P3
                  INNER JOIN Aeroport ON Aeroport_L = Aeroport.ID_AeroP
              ) as P4
              INNER JOIN Aeroline USING(ID_A)
        WHERE Date_Hour_S >= CURRENT_TIMESTAMP
        ORDER BY Date_Hour_S
        """,)

    conn = None
    result1 = None  

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result1

# Cliente: Ver reservar
def select_client_booking_flights(id_T):
    command = (
        f""" 
        SELECT Name_A FROM Booking INNER JOIN Client USING(ID_C) INNER JOIN Aeroline USING(ID_A) 
        WHERE ID_Telegram = {id_T}
        """,
        """ 
        SELECT COUNT(*) as Tickets_Booking FROM Booking GROUP BY (Cod_F, ID_C, Fecha_R)
        """,
        """ 
        SELECT * FROM Booking INNER JOIN Client USING(ID_C) INNER JOIN Flight USING(Cod_F)
        WHERE ID_Telegram = {id_T}
        """,
        """ 
        SELECT Seat FROM Booking INNER JOIN Client USING(ID_C) INNER JOIN Airfare USING(Cod_F, ID_CR) 
        WHERE ID_Telegram = {id_T}
        """,)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        cur.execute(command[2])
        result3 = cur.fetchall()

        cur.execute(command[3])
        result4 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result1, result2, result3, result4

#Cliente: Dado el ID_Aeropuerto de el nombre
def select_name_aeroport(ID_A):
    command = (
        f""" 
        SELECT Name_AeroP  FROM Aeroport WHERE ID_AeroP = {ID_A}
        """,)
    
    conn = None
    result = None

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result    

#Cliente: Dado el ID_Aerolinea de el nombre
def select_name_aeroline(ID_A):
    command = (
        f""" 
        SELECT Name_A FROM Aeroline WHERE ID_A = {ID_A}
        """,)
    
    conn = None
    result = None

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result    
    
# Gerente: Ver prereservas
def select_employee_booking(id_P):
    command = (
        f""" 
        SELECT Name_A FROM Prebooking INNER JOIN Aeroline USING(ID_A) 
        WHERE ID_P = {id_P}
        """,
        """ 
        SELECT COUNT(*) as Tickets_Prebooking FROM Prebooking GROUP BY (Cod_F, Fecha_R)
        """,
        """ 
        SELECT * FROM Prebooking INNER JOIN Flight USING(Cod_F)
        WHERE ID_P = {id_P}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        cur.execute(command[2])
        result3 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result1, result2, result3

# Gerente: Ver datos de la reservar (al pagar)
def select_employee_booking_flights(id_P):
    
    command = (
        f""" 
        SELECT Name_A FROM Booking INNER JOIN Aeroline USING(ID_A) 
        WHERE ID_P = {id_P}
        """,
        """ 
        SELECT COUNT(*) as Tickets_Booking FROM Booking GROUP BY (Cod_F, Fecha_R)
        """,
        """ 
        SELECT * FROM Booking INNER JOIN Flight USING(Cod_F)
        WHERE ID_P = {id_P}
        """,
        """ 
        SELECT Seat, Cost_Passage FROM Booking INNER JOIN Airfare USING(Cod_F, ID_CR) 
        WHERE ID_P = {id_P}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        cur.execute(command[2])
        result3 = cur.fetchall()

        cur.execute(command[3])
        result4 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result1, result2, result3, result4

# Empleado de Mostrador: Verificar cliente (DUDAS)
def select_client_for_checking(id_T, cod_f):

    command = (
        f""" 
        SELECT Name_C, Last_name_C, Country_C, Visa FROM Client INNE JOIN Passenger_Flow USING(ID_C)
        WHERE ID_Telegram = {id_T}
        """,
        """ 
        SELECT Name_A FROM Prebooking INNER JOIN Client USING(ID_C) INNER JOIN Aeroline USING(ID_A) 
        WHERE ID_Telegram = {id_T}
        """,
        """ 
        SELECT Seat FROM Airfare (DUDA: ok)
        """,
        """ 
        SELECT * FROM Booking INNER JOIN Client USING(ID_C) INNER JOIN Flight USING(Cod_F)
        WHERE ID_Telegram = {id_T} (DUDA: igual)
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        cur.execute(command[2])
        result3 = cur.fetchall()

        cur.execute(command[3])
        result4 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result1, result2, result3, result4

# Empleado de Puerta de Salida: Todos los pasajeros
def select_all_passengers(id_F):
    command = (
        f""" 
        SELECT ID_C, Name_C, Last_name_C 
        FROM (SELECT ID_C FROM Booking INNER JOIN Flight USING(Cod_F))
             INNER JOIN Client USING(ID_C)
        WHERE ID_Telegram = {id_T}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Operador de Vuelo: Ver naves segun su clasificacion
def select_all_nave_clasif(nave_clasif):
    command = (
        f""" 
        SELECT Enrollment, Clasif, Capacitance, No_Tripulante, Name_A
        FROM Nave INNER JOIN Aeroline USING(ID_A)
        WHERE Clasif = {nave_clasif}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Operador de Vuelo: Vuelos que entran
def select_all_flight_in():
    command = (
       f""" 
       SELECT Enrollment, Lugar_Origen, Fecha_Hora_L
       FROM Nave INNER JOIN Flight USING(ID_A)
       WHERE Fecha_Hora_L IN (SELECT * 
                              FROM Flight CONVERT(DATE, Fecha_Hora_L) 
                              WHERE Fecha_Hora_L = GETDATE())
       """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Operador de Vuelo: Vuelos que salen
def select_all_flight_out():
    command = (
        f""" 
        SELECT Enrollment, Lugar_Destino, Fecha_Hora_S
        FROM Nave INNER JOIN Flight USING(ID_A)
        WHERE Fecha_Hora_S IN (SELECT * 
                               FROM Flight CONVERT(DATE, Fecha_Hora_S) 
                               WHERE Fecha_Hora_S = GETDATE())
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Jefe del Departamento de Recursos Humanos: Eliminar empleado
def select_employee_to_eliminate(id_E):
    
    command = (
        f""" 
        SELECT * FROM Employee WHERE ID_E = {id_E}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Jefe del Departamento de Recursos Humanos: Listado de todos los empleados
def select_all_employee():
    command = (
        """ 
        SELECT * FROM Employee
        """,)
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

# Jefe del Departamento de Recursos Humanos: Todos los cargos que hay
def select_all_jobs():
    command = (
        """ 
        SELECT Office FROM Office
        """,
        )
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Jefe de Mecanica: Nave que se reparo
def select_nave_repaired(nave_clasif):

    command = (
        f""" 
        SELECT Enrollment, Clasif, Capacitance, No_Tripulante, Name_A, Tipo_R
        FROM Nave INNER JOIN Aeroline USING(ID_A) INNER JOIN Repair USING(Enrollment)
        WHERE Clasif = {nave_clasif}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Jefe de Almacen: Ver producto (DUDA): aunq tengan nombre iguales tendran ID distintos?
def select_product(id_Prod):
    command = (
        f""" 
        SELECT * FROM Product WHERE ID_Prod = {id_Prod}
        """,
        """
        SELECT COUNT(*) as Cant_Product FROM ID_Prod GROUP BY (Name_Prod) WHERE ID_Prod = {id_Prod}
        """,
        """
        SELECT Cost_Prod FROM Product INNER JOIN Product_Inst USING(ID_Prod) WHERE ID_Prod = {id_Prod}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        cur.execute(command[2])
        result3 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result1, result2, result3

# Supervisor de Instalaciones: Ver instalacion
def select_installation(name_i):
    command = (
        f""" 
        SELECT * FROM Installation WHERE Name_I = {name_i}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Empleado de Instalacion: Ver producto
def select_product(id_Prod):
    command = (
        f""" 
        SELECT ID_Prod, Name_Prod FROM Product WHERE ID_Prod = {id_Prod}
        """,
        """
        SELECT COUNT(*) as Cant_Product FROM ID_Prod GROUP BY (Name_Prod) WHERE ID_Prod = {id_Prod}
        """)

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        cur.execute(command[2])
        result3 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result1, result2, result3

# Obtener todos los aeropuertos
def select_all_aeroports():
    
    command = (
        f""" 
        SELECT * FROM Aeroport
        """)
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Obtener pasaporte del cliente
def select_passport_client(id_C):
    command = (
        f""" 
        SELECT No_Passport FROM Client WHERE ID_C = {id_C}
        """)
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Obtener id_c del cliente usando no_pasaporte
def select_ID_client_using_no_passport(no_passport):
    command = (
        f""" 
        SELECT ID_C FROM Client WHERE No_Passport = \'{no_passport}\'
        """,)
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

# Obtener pasaporte del cliente
def select_ID_client_using_id_telegram(id_telegram):
    command = (
        f""" 
        SELECT ID_C FROM Client WHERE ID_Telegram_C = {id_telegram}
        """, )
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

def select_ID_Flight(lo, ld, id_a, fecha):
    command = (
        f""" 
        SELECT ID_F FROM Flight WHERE ID_A = {id_a} AND Aeroport_S = {lo} AND Aeroport_L = {ld} AND Date_Hour_S = \'{fecha}\'
        """, )
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def select_all_clients():
    command = (
        """  
        SELECT ID_C, No_Passport FROM Client
        """,)
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def select_all_booking():
    command = (
        """  
        SELECT * FROM Booking
        """,)
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result

def select_flight_fo(Id_T):
    command = (
        f"""
        SELECT Enrollment, Clasif, Capacity, No_Tripulante, Total_Passenger FROM Flight INNER JOIN Flight_Matric USING(ID_F) INNER JOIN Airplane USING(Enrollment) 
        INNER JOIN Total_Passenger USING (Clasif, Capacity, No_Tripulante) WHERE Aeroport_S = (SELECT ID_AeroP FROM Employee WHERE ID_Telegram_E = \'{Id_T}\') or 
        Aeroport_L = (SELECT ID_AeroP FROM Employee WHERE ID_Telegram_E = \'{Id_T}\') GROUP BY Enrollment, Clasif, Capacity, No_Tripulante, Total_Passenger
        """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def select_flight_departures(Id_T):
    command = (
    f"""
        SELECT Cod_F, Enrollment, Name_A, Date_Hour_S, Aeroport_L FROM Flight INNER JOIN Aeroline USING(ID_A) INNER JOIN Flight_Matric USING(ID_F) 
        WHERE Aeroport_S = (SELECT ID_AeroP FROM Employee WHERE ID_Telegram_E = \'{Id_T}\') AND Date_Hour_S BETWEEN  CURRENT_TIMESTAMP + INTERVAL '1 hr' and  CURRENT_DATE + INTERVAL '1 day'
        ORDER BY Date_Hour_S; 
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def select_flight_enters(Id_T):
    command = (
    f"""
        SELECT Cod_F, Enrollment, Name_A, Date_Hour_L, Aeroport_S 
        FROM Flight INNER JOIN Aeroline USING(ID_A) INNER JOIN Flight_Matric USING(ID_F) WHERE Aeroport_L = (SELECT ID_AeroP 
        FROM Employee WHERE ID_Telegram_E = \'{Id_T}\') AND Date_Hour_L BETWEEN  CURRENT_TIMESTAMP + INTERVAL '1 hr' and  CURRENT_DATE + INTERVAL '1 day'
        ORDER BY Date_Hour_L; 
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result


def select_ID_A_employee_using_id_telegram(id_telegram):
    command = (
        f""" 
        SELECT ID_AeroP FROM Employee WHERE ID_Telegram_E = {id_telegram}
        """, )
    result = None
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchone()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

#esta demanda tambien la utilizamos para el empleado de mostrador 
def select_flight_departures_check_in_door(id_telegram):
    command = (
    f"""
        SELECT Cod_F, Date_Hour_S, Date_Hour_L, Name_A, a_s, Name_AeroP AS a_l, ID_F FROM
        (SELECT Cod_F, Date_Hour_S, Date_Hour_L, Name_A, Name_AeroP AS a_s, Aeroport_L, ID_F FROM Flight INNER JOIN Aeroline USING(ID_A) 
        INNER JOIN Aeroport ON Aeroport.ID_AeroP = Aeroport_S WHERE Aeroport_S = (SELECT ID_AeroP FROM Employee WHERE ID_Telegram_E = \'{id_telegram}\') AND Date_Hour_S BETWEEN CURRENT_DATE + INTERVAL '1 hr' AND  CURRENT_DATE + INTERVAL '1 day'
        ORDER BY Date_Hour_S) AS a1 INNER JOIN Aeroport ON Aeroport.ID_AeroP = Aeroport_L
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#esta demanda tambien la utilizamos para el empleado de mostrador 
def select_all_passengers_in_flight(ID_F):
    command = (
    f"""
        SELECT Name_C, Last_name_C, Country_C, No_Passport, ID_C FROM Airfare INNER JOIN Client USING(ID_C) INNER JOIN Flight USING(ID_F) WHERE ID_F = {ID_F} AND Count_Baggage is NULL
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#empleado de migracion
def select_all_passengers_in(id_T):
    command = (
    f"""
        SELECT Name_C, Last_name_C, Country_C, No_Passport, ID_C, ID_F FROM Flight INNER JOIN Airfare USING(ID_F) INNER JOIN Client USING(ID_C)
        INNER JOIN Passenger_Flow USING(ID_C, ID_F) WHERE Aeroport_L = (SELECT ID_AeroP 
        FROM Employee WHERE ID_Telegram_E = \'{id_T}\') AND Date_Hour_L BETWEEN  CURRENT_TIMESTAMP - INTERVAL '7 hr' and  CURRENT_TIMESTAMP + INTERVAL '7 hr'
        AND isAccepted_S = \'1\' AND isAccepted_E = NULL ORDER BY Date_Hour_L; 
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def select_all_passengers_on(id_T): #QUE NO ESTE EN LA TABLA                            
    command = (
    f"""
        SELECT Name_C, Last_name_C, Country_C, No_Passport, ID_C, ID_F FROM Flight INNER JOIN Airfare USING(ID_F) INNER JOIN Client USING(ID_C) WHERE Aeroport_S = (SELECT ID_AeroP 
        FROM Employee WHERE ID_Telegram_E = \'{id_T}\') AND Date_Hour_S BETWEEN  CURRENT_TIMESTAMP - INTERVAL '7 hr' and  CURRENT_TIMESTAMP + INTERVAL '7 hr' AND (ID_F, ID_C) NOT IN (SELECT ID_F, ID_C FROM Passenger_Flow)
        ORDER BY Date_Hour_S;  
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result
    
#empleado de mostrador
def select_client_data_and_his_flight(ID_F, ID_C):
    command = (
    f"""
        SELECT Name_C, Last_name_C, Country_C, No_Passport, ID_C, Flight.ID_F, Flight.Cod_F, Flight.Date_Hour_S, Flight.Date_Hour_L, Name_A, a_s, a_l FROM 
        Flight INNER JOIN Airfare USING(ID_F) INNER JOIN Client USING(ID_C) INNER JOIN 
        (SELECT Cod_F, Date_Hour_S, Date_Hour_L, Name_A, a_s, Name_AeroP AS a_l, ID_F FROM
        (SELECT Cod_F, Date_Hour_S, Date_Hour_L, Name_A, Name_AeroP AS a_s, Aeroport_L, ID_F FROM Flight INNER JOIN Aeroline USING(ID_A) 
        INNER JOIN Aeroport ON Aeroport.ID_AeroP = Aeroport_S) AS a1 INNER JOIN Aeroport ON Aeroport.ID_AeroP = Aeroport_L) AS a2 USING(ID_F) 
        WHERE ID_F = {ID_F} AND ID_C = {ID_C}
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#Gerente: listado de todos los empleados del aeropuerto
def select_all_employee_in_aeroports(ID_A):
    command = (
    f"""
        SELECT Name_E, Last_name_E, ID_E, Country_NE, DNI , Job FROM Employee WHERE ID_AeroP = \'{ID_A}\' GROUP BY ID_E
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def select_employee(id_E):
    command = (
    f"""
        SELECT * Employee WHERE ID_E = {ID_E}
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#Jefe de mecanica: Todas las naves
def select_all_airplanes(id_AeroP):
    command = (
        f"""
        SELECT Enrollment, Clasif, Capacity
        FROM Airplane INNER JOIN Apply_Repair USING(Enrollment)
        WHERE Apply_Repair.ID_AeroP = \'{id_AeroP}\'
        GROUP BY Enrollment
        """,)

    conn = None
    result1 = None  

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result1

#Jefe de mecanica: Reparaciones de una nave
def select_airplane_repairs(enrollment, id_AeroP, id_I):

    command = (
        f"""
        SELECT Enrollment, Clasif, Capacity, No_Tripulante, Name_C
        FROM (SELECT Enrollment, Clasif, Capacity, No_Tripulante, ID_C
              FROM(SELECT Enrollment, Clasif, Capacity, No_Tripulante
                   FROM Airplane INNER JOIN Apply_Repair USING(Enrollment)
                   WHERE Enrollment = \'{enrollment}\'
                   GROUP BY Enrollment
                   ) as P1
                   INNER JOIN Client_Matric USING(Enrollment)
              ) as P2
              INNER JOIN Client USING(ID_C)
        """,
        f"""
        SELECT Enrollment, Date_Begin, Date_End, Type_RR, P3.Cost_R, repair.Cost_R as Cost_R1 , Monto_Total + repair.Cost_R , ID_AeroP, Type_R as Typ_R1, Time, Cod_R1, ID_I
        FROM(SELECT Enrollment, Date_Begin, Date_End, Type_R as Type_RR, Cost_R, SUM(Cost_R) as Monto_Total, ID_AeroP, Cod_R1, Time, ID_I
             FROM(SELECT Enrollment, Date_Begin, Date_End, Type_R, Cost_R, Cod_R, ID_AeroP, Cod_R1, Time, ID_I
                  FROM(SELECT Cod_R, Cod_R1, Type_R, Cost_R
                       FROM Repair LEFT OUTER JOIN Need_Repair USING(Cod_R)
                      ) as P1
                      INNER JOIN Apply_Repair USING(Cod_R)
                 ) as P2
        WHERE Enrollment = \'{enrollment}\' AND ID_AeroP = \'{id_AeroP}\' AND ID_I = \'{id_I}\'
        GROUP BY Enrollment, Cod_R, Type_R, Cost_R, Cod_R1, Date_Begin, Date_End, Time, ID_AeroP, ID_I
        ) as P3
        LEFT OUTER JOIN Repair ON repair.cod_r = Cod_R1
        """,)

    conn = None
    result1 = None 
    result2 = None 

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()
        
        cur.execute(command[1])
        result2 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result1, result2

#Empleado de recursos humanos: lista de todas las instalaciones de un aeropuerto
def select_all_installation_in_a_aeroport(ID_A):
    command = (
    f"""
        SELECT ID_I, ID_AeroP, Name_I, Type FROM Installation WHERE ID_AeroP = \'{ID_A}\'
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#Jefe de almacen: lista de todos los productos de una instalacion
def select_all_products(ID_A, ID_I):
    command = (
    f"""
        SELECT ID_Prod, Name_Prod, Cost_Prod, Count_Prod 
        FROM Product_Installation INNER JOIN Product 
        USING(ID_AeroP, ID_I) 
        WHERE ID_AeroP = \'{ID_A}\' AND WHERE ID_I = \'{ID_I}\'
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result



def select_cant_product_inst(id_AeroP, id_I, id_Prod):
    command = (
    f"""
        SELECT Count_Prod 
        FROM Product_Installation 
        WHERE ID_AeroP = \'{id_AeroP}\' AND ID_I = \'{id_I}\' AND ID_Prod = \'{id_Prod}\'
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchone()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

    pass

def select_id_installation_employee(ID_Telegram_E):
    command = (
    f"""
        SELECT ID_I FROM Employee WHERE ID_Telegram_E = \'{ID_Telegram_E}\'
    """,
    )
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchone()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#Supervisor de instalaciones: Todas las instalaciones dado un aeropuerto
def select_all_installation_in_Supervisor(id_AeroP):
    command = (
        f"""
        SELECT Name_I, Type_I
        FROM Installation
        WHERE ID_AeroP = \'{id_AeroP}\'
        """,)

    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#Supervisor de instalaciones: Todos los tipos de instalaciones
def select_all_type_installation_in_Supervisor():
    command = (
        f"""
        SELECT Type
        FROM InstallationType
        """,)

    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

#Supervisor de instalaciones: instalacion especifica
def select_installation(id_AeroP, id_I):
    command = (
        f"""
        SELECT ID_I, Name_I, Type_I
        FROM Installation
        WHERE ID_I = \'{id_I}\' AND ID_AeroP = \'{id_AeroP}\'
        """,)

    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result

def select_the_last_product():
    command = (
        f""" 
        SELECT ID_Prod FROM Product ORDER BY ID_Prod DESC LIMIT 1
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

#Empleado de instalacion: Todos los productos de la instalacion
def select_all_product_employee_inst(id_I, id_AeroP):
    command = (
        f""" 
        SELECT ID_Prod, Name_Prod, Cost_Prod, Count_Prod
        FROM Product INNER JOIN Product_Installation USING(ID_Prod)
        WHERE ID_I = \'{id_I}\' AND ID_AeroP = \'{id_AeroP}\'
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

#Empleado de instalacion: Obtener datos de un producto
def select_product(id_Prod, id_I):
    command = (
        f""" 
        SELECT ID_Prod, Name_Prod, Cost_Prod, Count_Prod
        FROM Product INNER JOIN Product_Installation USING(ID_Prod)
        WHERE ID_I = \'{id_I}\' AND ID_I = \'{id_I}\'
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

def select_the_last_buy():
    command = (
        """ 
        SELECT ID_Buy FROM Buy ORDER BY ID_Buy DESC LIMIT 1
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

def select_installation_info(id_I, id_AeroP):
    command = (
        f""" 
        SELECT Name_I, Type FROM Installation WHERE ID_I = \'{id_I}\' AND ID_AeroP = \'{id_AeroP}\'
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

#Gerente: Ver prereserva
def select_booking_gerente():
    command = (
        f"""
        SELECT ID_B, Date_booking, Cod_F, Name_A, COUNT(ID_B), Aero_S, Aero_L, Date_Hour_S, Date_Hour_L, Price
        FROM (SELECT ID_B, Date_booking, Cod_F, Name_A, Aero_S, Aero_L, Date_Hour_S, Date_Hour_L, Price
                    FROM(SELECT ID_B, Date_booking, Cod_F, ID_A, Aero_S, Name_AeroP as Aero_L, Date_Hour_S, Aeroport_L, Date_Hour_L, Price
                         FROM (SELECT ID_B, Date_booking, Cod_F, ID_A , Name_AeroP as Aero_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price
                               FROM(SELECT IS_paid, ID_B, Date_booking, Cod_F, ID_A , Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price
                                    FROM(SELECT ID_B, ID_F, Date_booking, IS_paid
                                         FROM Client INNER JOIN Booking USING(ID_C)
                                        ) as P1 INNER JOIN Flight USING(ID_F)
                                    WHERE IS_paid = '0'
                                    ) as P2
                                    INNER JOIN Aeroport ON Aeroport_S = Aeroport.ID_AeroP
                               ) as P3
                               INNER JOIN Aeroport ON Aeroport_L = Aeroport.ID_AeroP
                        ) as P4 
                        INNER JOIN Aeroline USING(ID_A)
              ) as P5 INNER JOIN BookingTo USING(ID_B)
        WHERE Date_booking <= Date_booking + interval '1 hours'
        GROUP BY ID_B, Date_booking, Cod_F, Name_A, Aero_S, Aero_L, Date_Hour_S, Date_Hour_L, Price
        ORDER BY Date_booking
        """,
        f"""
        DELETE 
        FROM Booking 
        WHERE Date_booking > Date_booking + interval '1 hours'
        """,)

    conn = None
    result1 = None
    result2 = None

    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result1 = cur.fetchall()

        cur.execute(command[1])
        result2 = cur.fetchall()

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return result1

def select_no_passaport_the_all_booking():
    command = (
        f""" 
        SELECT No_Passport FROM Booking INNER JOIN Client USING(ID_C)
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result 

def select_all_booking_for_a_no_passaport(no_passaport):
    command = (
        f""" 
        SELECT No_Passport FROM Booking INNER JOIN Client USING(ID_C) WHERE IS_paid = \'0\'
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result 

def select_Booking_not_paid():
    command = (
        f""" 
        SELECT ID_B, ID_C, ID_F,  Date_booking, Cod_F, a_s, Date_Hour_S, Name_AeroP as a_l, Date_Hour_L, Price FROM
        (SELECT ID_B, ID_C, ID_F , Date_booking, Cod_F, Name_AeroP a_s, Date_Hour_S, Aeroport_L, Date_Hour_L, Price FROM
        (SELECT ID_B, ID_C, ID_F , Date_booking, Cod_F, Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price FROM Booking INNER JOIN Flight USING(ID_F) 
        WHERE IS_paid = \'0\') AS p1 INNER JOIN  Aeroport ON p1.Aeroport_S = Aeroport.ID_AeroP) as p2 INNER JOIN Aeroport ON p2.Aeroport_L = Aeroport.ID_AeroP
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

def select_Booking(id_B):
    command = (
        f""" 
        SELECT ID_B, ID_C, ID_F,  Date_booking, Cod_F, a_s, Date_Hour_S, Name_AeroP as a_l, Date_Hour_L, Price FROM
        (SELECT ID_B, ID_C, ID_F , Date_booking, Cod_F, Name_AeroP a_s, Date_Hour_S, Aeroport_L, Date_Hour_L, Price FROM
        (SELECT ID_B, ID_C, ID_F , Date_booking, Cod_F, Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price FROM Booking INNER JOIN Flight USING(ID_F) 
        WHERE IS_paid = \'0\' AND ID_B = \'{id_B}\')  AS p1 INNER JOIN  Aeroport ON p1.Aeroport_S = Aeroport.ID_AeroP) as p2 INNER JOIN Aeroport ON p2.Aeroport_L = Aeroport.ID_AeroP
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

def select_repair_type():
    command = (
        f""" 
            SELECT * FROM repair
        """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        cur.execute(command[0])
        result = cur.fetchall()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result 

def select_cant_prod(ID_A, ID_I, Cod_Prod):
    command = (
    f""" 
        SELECT Count_Prod
        FROM Product INNER JOIN Product_Installation USING(ID_Prod)
        WHERE ID_I = \'{ID_I}\' AND ID_AeroP = \'{ID_A}\' AND ID_Prod = \'{Cod_Prod}\'
    """,)
    
    conn = None
    result = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        result = cur.fetchone()
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return result 
