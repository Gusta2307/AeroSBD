import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """ 
        CREATE TABLE IF NOT EXISTS Client (
            ID_C INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Name VARCHAR(50) NOT NULL,
            Last_name VARCHAR(50) NOT NULL,
            Country_C VARCHAR(50) NOT NULL,
            ID_Telegram INTEGER NOT NULL  
        ))
        """,
        """ 
        CREATE TABLE IF NOT EXISTS Aeroline (
            ID_A PRIMARY KEY AUTOINCREMENT NOT NULL,
            Name VARCHAR(50) NOT NULL,
            Country_N VARCHAR(50) NOT NULL
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS Employee (
            ID_E PRIMARY KEY  NOT NULL,
            ID_Telegram INTEGER,
            Name VARCHAR(50) NOT NULL,
            Country_N VARCHAR(50) NOT NULL,
            Job VARCHAR(50) NOT NULL
        )
        """
        #CREATE TABLE vendor_parts (
        #        vendor_id INTEGER NOT NULL,
        #        part_id INTEGER NOT NULL,
        #        PRIMARY KEY (vendor_id , part_id),
        #        FOREIGN KEY (vendor_id)
        #            REFERENCES vendors (vendor_id)
        #            ON UPDATE CASCADE ON DELETE CASCADE,
        #        FOREIGN KEY (part_id)
        #            REFERENCES parts (part_id)
        #            ON UPDATE CASCADE ON DELETE CASCADE
        #)
        #"""
        )
    conn = None #esto no creo que haga falta
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()