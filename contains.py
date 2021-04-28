import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def contains_user_start(id_T):
    command = (
        f""" 
        SELECT ID_Telegram FROM Client WHERE ID_Telegram = {id_T}
        """,
        f"""
        SELECT ID_Telegram, Job FROM Employee WHERE ID_Telegram = {id_T}
        """)
    User = None
    result = ""
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        
        cur.execute(command[0])
        print(command[0])
        User = cur.fetchall()
        print(User)
        if User != None:
            result = "Cliente"
        
        cur.execute(command[1])
        print(command[1])
        User = cur.fetchall()
        print(User)
        if User != None and len(User) > 1:
            result = f"Empleado_{User[1]}"
        print(result)
        # close communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return result