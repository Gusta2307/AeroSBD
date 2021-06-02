import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")


sql = """INSERT INTO Employee(Name_E, Last_name_E, Country_NE, ID_Telegram_E, Job, DNI, ID_AeroP)
            VALUES(%s,%s,%s,%s,%s,%s, %s)"""

sql0 =   """ 
        UPDATE Employee SET Job = %s  WHERE ID_Telegram_E = %s
        """

sql00 =   """ 
        UPDATE Employee SET ID_I = %s  WHERE ID_Telegram_E = %s
        """

sql1 = """
        INSERT INTO Flight(ID_A, Cod_F, Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price) VALUES
        (1, 16093, 10, '2021-05-29 20:30', 11, '2021-05-29 22:30', 4366)
        """

sql2 = """
        INSERT INTO Flight_Matric (Enrollment, ID_F) VALUES
        ('EC-23001', 13)
        """
    
sql3 = """
        INSERT INTO Flight_Matric (Enrollment, ID_F) VALUES
        ('N62941', 12);
        """

sql4 = """
        INSERT INTO Booking (ID_C, ID_F, Date_booking, IS_paid) VALUES
        (1, 13, '2021-05-29 01:30', 1)
        """

sql5 = """
        INSERT INTO BookingTo(ID_B, ID_C) VALUES
        (25, 1)
        """

sql6 = """
        INSERT INTO Airfare(ID_C, ID_F, Count_Baggage) VALUES
        (1, 12, 4),
        (2, 12, 4)
        """

conn = None
try:
    # connect to the PostgreSQL database
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # create a new cursor
    cur = conn.cursor()
    #937372768
    # execute the INSERT statement
    #cur.execute(sql4,)
    #cur.execute(sql6,)
    #cur.execute(sql, ("GDD", "MC", "Cuba", 1439731435, "employee_humanResources", 99, 10))
    #cur.execute(sql, ("SAF", "MC", "Cuba", 937372768, "employee_salesManager", 99))
    #cur.execute(sql0,("employee_installation", 716780131))
    cur.execute(sql0,("employee_chiefMachanic", 937372768))
    #cur.execute("DELETE FROM Employee WHERE ID_Telegram_E = %s", (716780131,))
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

print("AAAAAAAAAA")

#sql = """INSERT INTO Office(Office, Salary)
#            VALUES(%s,%s)"""
#conn = None
#try:
#    # connect to the PostgreSQL database
#    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#    # create a new cursor
#    cur = conn.cursor()
#    # execute the INSERT statement
#    cur.execute(sql, ("Gerente de Ventas", 256))
#    cur.execute(sql, ("Empleado de Mostrador", 24.8))
#    cur.execute(sql, ("Empleado de Migracion", 2344))
#    cur.execute(sql, ("Empleado de Puerta de Salida", 445.8))
#    cur.execute(sql, ("Operador de Vuelo", 3545))
#    cur.execute(sql, ("Empleado de Recursos Humanos", 765))
#    cur.execute(sql, ("Jefe de Mecanica", 7634))
#    cur.execute(sql, ("Jefe de Almacen", 4657))
#    cur.execute(sql, ("Jefe de Supervisor de Instalaciones", 4543.8))
#    cur.execute(sql, ("Empleado de Instalacion", 4543.8))
#    
#    # commit the changes to the database 
#    conn.commit()
#    # close communication with the database
#    cur.close()
#except (Exception, psycopg2.DatabaseError) as error:
#    print(error)
#finally:
#    if conn is not None:
#        conn.close()
