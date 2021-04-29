import psycopg2
import os

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

def insert_cliente(update, context):
    name = context.user_data["name"]
    last_name = context.user_data["last_name"]
    country = context.user_data["country"]
    id_telegram = update._effective_chat.id

    query = f""" 
            INSERT INTO Client(Name_C, Last_name_C, Country_C, ID_Telegram)
            VALUES ({name}, {last_name}, {country}, {id_telegram});
        """
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()