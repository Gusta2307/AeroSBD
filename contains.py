import psycopg2
import os 

DATABASE_URL = os.environ.get("DATABASE_URL")

def isRegistered(id_T):
    id_T = int(id_T)
    command = (
        f""" 
        SELECT ID_Telegram_C FROM Client WHERE ID_Telegram_C = {id_T}
        """,
        f"""
        SELECT ID_Telegram_E, Job FROM Employee WHERE ID_Telegram_E = {id_T}
        """)
    User = None
    result = ""
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        cur.execute(command[0])
        User = cur.fetchall()
        if User != []:
            result = "client"
        
        cur.execute(command[1])
        User = cur.fetchall()
        if User != []:
            result = f"{User[0][1]}"
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result

def contains_client(no_passager):
    command = (
        f""" 
        SELECT ID_C, ID_Telegram_C FROM Client WHERE No_Passport = \'{str(no_passager)}\'
        """,
        )
    User = None
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

def isCodeCorrect(code):
    command = (
        f""" 
            SELECT ID_E, Job FROM Employee WHERE Cod_verif = {code}
        """,
        )
    result = []
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(command[0])
        employee = cur.fetchall()
        if employee != []:
            result = employee

        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result