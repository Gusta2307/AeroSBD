import psycopg2
import os

DATABASE_URL = os.environ.get("DATABASE_URL")

def create_tables():
    """ create tables in the PostgreSQL database """
    commands = (
        """
        CREATE TABLE IF NOT EXISTS Aeroport(
            ID_AeroP SERIAL PRIMARY KEY,
            Name_AeroP VARCHAR(50) NOT NULL,
            Pos_Geog VARCHAR(80) NOT NULL,
            Direction VARCHAR(100) NOT NULL
        )
        """,
        """
         CREATE TABLE IF NOT EXISTS InstallationType(
            Type VARCHAR(50) PRIMARY KEY
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Date(
            Date_Begin timestamp PRIMARY KEY NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Installation(
            ID_I SERIAL,
            ID_AeroP INTEGER NOT NULL,
            Name_I VARCHAR(50) NOT NULL,
            Type VARCHAR(50) NOT NULL,
            PRIMARY KEY(ID_I, ID_AeroP),
            FOREIGN KEY (ID_AeroP)
                REFERENCES Aeroport (ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Type)
                REFERENCES InstallationType(Type)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Aeroline(
            ID_A SERIAL PRIMARY KEY NOT NULL,
            Name_A VARCHAR(50) NOT NULL,
            Country_NA VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Airplane(
            Enrollment VARCHAR(50) PRIMARY KEY NOT NULL,
            Clasif VARCHAR(50) NOT NULL,
            Capacity INTEGER NOT NULL,
            No_Tripulante INTEGER NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Total_Passenger(
            Clasif VARCHAR(50) NOT NULL,
            Capacity INTEGER NOT NULL,
            No_Tripulante INTEGER NOT NULL,
            PRIMARY KEY(Clasif, Capacity, No_Tripulante),
            Total_Passenger INTEGER NULL
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS Client(
            ID_C SERIAL PRIMARY KEY,
            Name_C VARCHAR(50) NOT NULL,
            Last_name_C VARCHAR(50) NOT NULL,
            Country_C VARCHAR(50) NOT NULL,
            ID_Telegram_C INTEGER,
            No_Passport VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Flight(
            ID_F SERIAL PRIMARY KEY NOT NULL,
            ID_A INTEGER NOT NULL,
            Cod_F INTEGER NOT NULL,
            Aeroport_S INTEGER NOT NULL,
            Date_Hour_S timestamp NOT NULL,
            Aeroport_L INTEGER NOT NULL,
            Date_Hour_L timestamp NOT NULL,
            Price FLOAT8 NOT NULL,
            FOREIGN KEY (ID_A)
                REFERENCES Aeroline (ID_A)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Aeroport_S)
                REFERENCES Aeroport (ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Aeroport_L)
                REFERENCES Aeroport (ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Booking(
            ID_B SERIAL PRIMARY KEY,
            ID_C INTEGER NOT NULL,
            ID_F INTEGER NOT NULL,
            Date_booking timestamp NOT NULL, 
            IS_paid INTEGER NOT NULL,
            FOREIGN KEY (Date_booking)
                REFERENCES Date (Date_Begin)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS BookingTo(
            ID_B INTEGER NOT NULL,
            ID_C INTEGER NOT NULL,
            PRIMARY KEY(ID_B, ID_C),
            FOREIGN KEY (ID_B)
                REFERENCES Booking(ID_B)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_C)
              REFERENCES Client (ID_C)
              ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Buy(
            ID_Buy SERIAL PRIMARY KEY,
            Date_Buy timestamp NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Product(
            ID_Prod SERIAL PRIMARY KEY,
            Name_Prod VARCHAR(50) NOT NULL,
            Cost_Prod INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Repair(
            Cod_R INTEGER PRIMARY KEY NOT NULL,
            Type_R VARCHAR(50) NOT NULL,
            Cost_R INTEGER NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Need_Repair(
            Cod_R INTEGER NOT NULL,
            Cod_R1 INTEGER NOT NULL,
            PRIMARY KEY(Cod_R, Cod_R1),
            FOREIGN KEY (Cod_R)
                REFERENCES Repair (Cod_R)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Apply_Repair(
            Enrollment VARCHAR(50) NOT NULL,
            Cod_R INTEGER NOT NULL,
            Date_Begin timestamp NOT NULL,
            Date_End timestamp NOT NULL,
            Time INTEGER NOT NULL,
            ID_AeroP INTEGER NOT NULL,
            ID_I INTEGER NOT NULL,
            PRIMARY KEY(Cod_R, Date_Begin, Enrollment),
            FOREIGN KEY (Cod_R)
                REFERENCES Repair (Cod_R)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Date_Begin)
                REFERENCES Date (Date_Begin)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (Enrollment)
                REFERENCES Airplane (Enrollment)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_I, ID_AeroP)
                REFERENCES Installation (ID_I, ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Product_Installation(
            ID_AeroP INTEGER NOT NULL,
            ID_I INTEGER NOT NULL,
            ID_Prod INTEGER NOT NULL,
            Count_Prod INTEGER NOT NULL,
            PRIMARY KEY(ID_Prod, ID_AeroP, ID_I),
            FOREIGN KEY (ID_Prod)
                REFERENCES Product (ID_Prod)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_I, ID_AeroP)
                REFERENCES Installation (ID_I, ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Employee(
            ID_E SERIAL PRIMARY KEY,
            Name_E VARCHAR(50) NOT NULL,
            Last_name_E VARCHAR(50) NOT NULL,
            Country_NE VARCHAR(50) NOT NULL,
            ID_Telegram_E INTEGER,
            Cod_Verif VARCHAR(50),
            Job VARCHAR(50) NULL,
            DNI BIGINT NOT NULL, 
            ID_AeroP INTEGER NOT NULL,
            ID_I INTEGER,
            FOREIGN KEY (ID_AeroP)
                REFERENCES Aeroport (ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_AeroP, ID_I)
                REFERENCES Installation (ID_AeroP, ID_I)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Aeroline_Matric(
            Enrollment VARCHAR(50) PRIMARY KEY NOT NULL,
            ID_A INTEGER NOT NULL,
            FOREIGN KEY (Enrollment)
                REFERENCES Airplane (Enrollment)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_A)
                REFERENCES Aeroline (ID_A)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Client_Matric(
            Enrollment VARCHAR(50) PRIMARY KEY NOT NULL,
            ID_C INTEGER NOT NULL,
            FOREIGN KEY (Enrollment)
                REFERENCES Airplane (Enrollment)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_C)
                REFERENCES Client (ID_C)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Flight_Matric(
            ID_F INTEGER PRIMARY KEY NOT NULL,
            Enrollment VARCHAR(50) NOT NULL,
            FOREIGN KEY (Enrollment)
                REFERENCES Airplane (Enrollment)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_F)
                REFERENCES Flight (ID_F)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Passenger_Flow(
            ID_C INTEGER NOT NULL,
            ID_F INTEGER NOT NULL,
            isAccepted_E INTEGER,
            isAccepted_S INTEGER NOT NULL,
            PRIMARY KEY(ID_C, ID_F),
            FOREIGN KEY (ID_C)
                REFERENCES Client (ID_C)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_F)
                REFERENCES Flight (ID_F)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Airfare(
            ID_C INTEGER NOT NULL,
            ID_F INTEGER NOT NULL,
            Count_Baggage INTEGER,
            PRIMARY KEY(ID_C, ID_F),
            FOREIGN KEY (ID_C)
                REFERENCES Client (ID_C)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_F)
                REFERENCES Flight (ID_F)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Product_Buy(
            ID_Prod INTEGER NOT NULL,
            ID_Buy INTEGER NOT NULL,
            Count_Prod INTEGER NULL,
            ID_I INTEGER NOT NULL,
            ID_AeroP INTEGER NOT NULL,
            PRIMARY KEY(ID_Prod, ID_Buy, ID_I, ID_AeroP),
            FOREIGN KEY (ID_Prod)
                REFERENCES Product (ID_Prod)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_Buy)
                REFERENCES Buy (ID_Buy)
                ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (ID_I, ID_AeroP)
                REFERENCES Installation (ID_I, ID_AeroP)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Office(
            Office VARCHAR(50) PRIMARY KEY,
            Salary Float(8) NOT NULL
        )
        """
        )
        
    conn = None 
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