import psycopg2
import os 

DATABASE_URL = os.environ.get("DATABASE_URL")


def delete_employee(id_E):
    command = (
    f"""
        DELETE FROM Employee WHERE ID_E = \'{id_E}\';
    """,
    )
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(command[0])
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def delete_booking(ID_B):
    command = (
    f"""
        DELETE FROM Booking WHERE ID_B = \'{ID_B}\';
    """,
    f"""
        DELETE FROM BookingTo WHERE ID_B = \'{ID_B}\';
    """,
    )
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(command[0])
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()