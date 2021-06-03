import psycopg2
import os
import random
from string import ascii_letters, ascii_uppercase, digits

DATABASE_URL = os.environ.get("DATABASE_URL")

def insert_aeroport_data():
    query = \
    """
    INSERT INTO Aeroport (Name_AeroP, Pos_Geog, Direction) VALUES
    ('Rey Khalid', 'Arabia Saudita', 'a 35 km de Riad'),
    ('Montreal-Mirabel ', 'Canadá', 'a 39 km al noroeste de Montreal'),
    ('Hartsfield-Jackson', 'Atlanta', 'a 11 km al sur del Distrito de Atlanta'),
    ('Chicago-OHare', 'EEUU', 'a 27 km al noroeste del Centro de Chicago'),
    ('John F. Kennedy', 'EEUU', 'a unos 20 km de Manhattan'),
    ('Los Ángeles', 'EEUU', 'a 27 km del centro'),
    ('Memphis', 'EEUU', 'a 5 km al sur de la ciudad de Memphis'),
    ('Bangda', 'China', '4.334 metros sobre el nivel del mar'),
    ('Barra', 'Reino Unido', 'en la ancha bahía de Traigh Mhor'),
    ('Gibraltar', 'España', 'a 1000 metros del casco urbano de Gibraltar'),
    ('Juan Santamaría', 'Costa Rica', 'a 18 km de la ciudad de San José'),
    ('Ministro Pistarini', 'Argentina', 'a unos 35 km al sudoeste de la ciudad de Buenos Aires'),
    ('São Paulo – Governador André Franco Montoro', 'Brasil', 'a 22 km al noreste de São Paulo'),
    ('El Dorado', 'Colombia', 'a 13,35 km al occidente del centro'),
    ('Miami', 'EEUU', 'a 13 km al noroeste del centro de Miami'),
    ('Inca Manco Cápac', 'Perú', 'a 3825 msnm'),
    ('Adolfo Suárez Madrid-Barajas', 'España', 'Paracuellos de Jarama'),
    ('Cancún', 'México', 'a 16 km de la ciudad de Cancún'),
    ('Halifax Robert L. Stanfield', 'Canadá', 'en Enfield, Nueva Escocia'),
    ('Edmonton', 'Canadá', 'a 14 MN al sudeste del centro de la ciudad de Edmonton'), 
    ('Regina', 'Canadá', 'a 7 km del centro de la ciudad'), 
    ('Kelowna', 'Canadá', '11.5 km al noreste de Kelowna'), 
    ('Ottawa/McDonald-Cartier', 'Canadá', 'a 10.2 km al sudeste del centro de la ciudad'), 
    ('San Bernardino ', 'EEUU', 'a 3 km al sur este del centro de San Bernardino'), 
    ('Ronald Reagan de Washington', 'EEUU', '7 km al sur de Washington D. C.'), 
    ('José Martí', 'Cuba', '18 km de La Habana'), 
    ('Abel Santamaría', 'Cuba', 'en la región central de la isla en la Provincia de Villa Clara'),
    ('Ignacio Agramonte', 'Cuba', 'en Avenida Finlay, Albaisa. Municipio Camagüey.'), 
    ('Charles de Gaulle', 'Francia', '25 km al noreste de París'), 
    ('Leonardo da Vinci', 'Italia', '34 km del centro histórico de Roma');
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute  the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_installation_data():
    query = \
    """
    INSERT INTO Installation (ID_AeroP, Name_I, Type) VALUES 
    (10, 'Zona de Reparaciones', 'Taller'),
    (10, 'Zona de Reparaciones', 'Taller'),
    (2, 'Zona de Reparaciones', 'Taller'),
    (3, 'Zona de Reparaciones', 'Taller'),
    (7, 'Zona de Reparaciones', 'Taller'),
    (2, 'Zona de Reparaciones', 'Taller'),
    (1, 'Zona de Reparaciones', 'Taller'),
    (5, 'Zona de Reparaciones', 'Taller'),
    (18, 'Zona de Reparaciones', 'Taller'),
    (17, 'McDonals', 'Alimentación'),
    (5, 'McDonals', 'Alimentación'),
    (9, 'McDonals', 'Alimentación'),
    (2, 'McDonals', 'Alimentación'),
    (30, 'McDonals', 'Alimentación'),
    (20, 'Domino´s', 'Alimentación'),
    (23, 'Domino´s', 'Alimentación'),
    (13, 'Domino´s', 'Alimentación'),
    (10, 'Domino´s', 'Alimentación'),
    (25, 'Domino´s', 'Alimentación'),
    (1, 'Domino´s', 'Alimentación'),
    (29, 'Domino´s', 'Alimentación'),
    (2, 'KFC', 'Alimentación'),
    (15, 'KFC', 'Alimentación'),
    (30, 'KFC', 'Alimentación'),
    (29, 'KFC', 'Alimentación'),
    (18, 'KFC', 'Alimentación'),
    (18, 'Burger King', 'Alimentación'),
    (16, 'Burger King', 'Alimentación'),
    (21, 'Burger King', 'Alimentación'),
    (8, 'Burger King', 'Alimentación'),
    (15, 'PizzaHut', 'Alimentación'),
    (8, 'PizzaHut', 'Alimentación'),
    (7, 'PizzaHut', 'Alimentación'),
    (5, 'Starbucks', 'Alimentación'),
    (4, 'Starbucks', 'Alimentación'),
    (23, 'Starbucks', 'Alimentación'),
    (12, 'Starbucks', 'Alimentación'),
    (14, 'Starbucks', 'Alimentación'),
    (8, 'Coffee Shop', 'Alimentación'),
    (4, 'Coffee Shop', 'Alimentación'),
    (11, 'Coffee Shop', 'Alimentación'),
    (17, 'SunGlass', 'Comercio'),
    (9, 'SunGlass', 'Comercio'),
    (7, 'SunGlass', 'Comercio'),
    (1, 'SunGlass', 'Comercio'),
    (10, 'SunGlass', 'Comercio'),
    (15, 'SunGlass', 'Comercio'),
    (20, 'SunGlass', 'Comercio'),
    (18, 'SunGlass', 'Comercio'),
    (25, 'SunGlass', 'Comercio'),
    (22, 'Adidas', 'Comercio'),
    (4, 'Adidas', 'Comercio'),
    (16, 'Adidas', 'Comercio'),
    (12, 'Adidas', 'Comercio'),
    (24, 'Puma', 'Comercio'),
    (14, 'Puma', 'Comercio'),
    (4, 'Puma', 'Comercio'),
    (23, 'Nike', 'Comercio'),
    (1, 'Nike', 'Comercio'),
    (3, 'Nike', 'Comercio'),
    (23, 'Nike', 'Comercio'),
    (5, 'Nike', 'Comercio'),
    (13, 'Converse', 'Comercio'),
    (23, 'Converse', 'Comercio'),
    (1, 'Converse', 'Comercio'),
    (5, 'Converse', 'Comercio'),
    (7, 'Converse', 'Comercio'),
    (9, 'Converse', 'Comercio'),
    (10, 'Converse', 'Comercio'),
    (15, 'Converse', 'Comercio'),
    (15, 'NB', 'Comercio'),
    (6, 'NB', 'Comercio'),
    (29, 'NB', 'Comercio'),
    (16, 'Lee', 'Comercio'),
    (14, 'Lee', 'Comercio'),
    (11, 'Lee', 'Comercio'),
    (12, 'Lee', 'Comercio'),
    (17, 'CuidadoConElPerro', 'Comercio'),
    (6, 'Samsung', 'Comercio'),
    (12, 'Samsung', 'Comercio'),
    (14, 'Samsung', 'Comercio'),
    (17, 'Samsung', 'Comercio'),
    (21, 'Samsung', 'Comercio'),
    (16, 'Samsung', 'Comercio'),
    (1, 'Apple', 'Comercio'),
    (3, 'Apple', 'Comercio'),
    (6, 'Apple', 'Comercio'),
    (26, 'Baño de Mujeres', 'Aseo'),
    (27, 'Baño de Mujeres', 'Aseo'),
    (28, 'Baño de Mujeres', 'Aseo'),
    (2, 'Baño de Mujeres', 'Aseo'),
    (27, 'Baño de Hombres', 'Aseo'),
    (28, 'Baño de Hombres', 'Aseo'),
    (26, 'Baño de Hombres', 'Aseo'),
    (3, 'Baño de Hombres', 'Aseo'),
    (4, 'Baño de Impedidos', 'Aseo'),
    (14, 'Baño de Impedidos', 'Aseo'),
    (23, 'Baño de Impedidos', 'Aseo'),
    (14, 'Baño de Impedidos', 'Aseo'),
    (16, 'Baño de Impedidos', 'Aseo'),
    (18, 'Baño de Impedidos', 'Aseo'),
    (17, 'Banco San Jorge', 'Finanzas'),
    (13, 'Banco San Jorge', 'Finanzas'),
    (25, 'Banco San Jorge', 'Finanzas'),
    (14, 'Banco San Jorge', 'Finanzas'),
    (11, 'Banco San Jorge', 'Finanzas'),
    (13, 'Banco San Jorge', 'Finanzas'),
    (4, 'Banco San Jorge', 'Finanzas'),
    (12, 'Banc Wells Fargo', 'Finanzas'),
    (10, 'Banc Wells Fargo', 'Finanzas'),
    (1, 'Banc Wells Fargo', 'Finanzas'),
    (1, 'Banc Chase', 'Finanzas'),
    (3, 'Banc Chase', 'Finanzas'),
    (7, 'Banc Chase', 'Finanzas'),
    (8, 'Banc of America', 'Finanzas'),
    (12, 'Banc of America', 'Finanzas'),
    (1, 'Banc of America', 'Finanzas'),
    (3, 'Citibanc', 'Finanzas'),
    (6, 'Citibanc', 'Finanzas'),
    (8, 'Citibanc', 'Finanzas'),
    (13, 'Citibanc', 'Finanzas'),
    (9, 'N26', 'Finanzas'),
    (13, 'N26', 'Finanzas'),
    (26, 'Cajas de Cambio', 'Finanzas'),
    (27, 'Cajas de Cambio', 'Finanzas'),
    (28, 'Cajas de Cambio', 'Finanzas'),
    (30, 'Cajas de Cambio', 'Finanzas'),
    (29, 'Cajas de Cambio', 'Finanzas'),
    (1, 'Cajas de Cambio', 'Finanzas'),
    (3, 'Cajas de Cambio', 'Finanzas'),
    (18, 'Cajas de Cambio', 'Finanzas'),
    (19, 'Cajas de Cambio', 'Finanzas'),
    (23, 'Banda de Equipaje', 'Aduana'),
    (12, 'Banda de Equipaje', 'Aduana'),
    (21, 'Banda de Equipaje', 'Aduana'),
    (17, 'Estacionamiento', 'Estacionamiento de automóviles'),
    (26, 'Estacionamiento', 'Estacionamiento de automóviles'),
    (27, 'Estacionamiento', 'Estacionamiento de automóviles'),
    (28, 'Estacionamiento', 'Estacionamiento de automóviles'),
    (1, 'Zona de Aparcamiento de Aviones', 'Aereo'), 
    (19, 'Zona de Aparcamiento de Aviones', 'Aereo'), 
    (24, 'Zona de Aparcamiento de Aviones', 'Aereo'), 
    (24, 'Sala de Embarque', 'Aduana'),
    (24, 'Sala de Embarque', 'Aduana'),
    (28, 'Zona de Reparaciones', 'Taller'),
    (6, 'Zona de Reparaciones', 'Taller'),
    (3, 'Zona de Reparaciones', 'Taller'),
    (9, 'Zona de Reparaciones', 'Taller'),
    (11, 'Zona de Reparaciones', 'Taller'),
    (14, 'Zona de Reparaciones', 'Taller'),
    (21, 'Zona de Reparaciones', 'Taller'),
    (4, 'Zona de Reparaciones', 'Taller'),
    (13, 'Zona de Reparaciones', 'Taller'),
    (28, 'Zona de Abastecimiento', 'Abastecedor'),
    (1, 'Zona de Abastecimiento', 'Abastecedor'),
    (6, 'Zona de Abastecimiento', 'Abastecedor'),
    (1, 'Zona de Reparaciones', 'Taller'),
    (2, 'Zona de Abastecimiento', 'Abastecedor'),
    (25, 'Zona de Reparaciones', 'Taller'),
    (24, 'Zona de Abastecimiento', 'Abastecedor'),
    (23,'Torre de Control', 'Aereo'), 
    (26, 'Zona de Reparaciones', 'Taller');
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_InstallationType_data():
    query = \
    """
    INSERT INTO InstallationType(Type) VALUES 
    ('Alimentación'),
    ('Comercio'),
    ('Aseo'),
    ('Finanzas'),
    ('Aduana'),
    ('Estacionamiento de automóviles'),
    ('Aereo'),
    ('Taller'),
    ('Abastecedor');
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_aeroline_data():
    query = \
    """
    INSERT INTO Aeroline (Name_A, Country_NA) VALUES 
    ('Cubana de Aviancion', 'Cuba'),
    ('Iberia', 'España'),
    ('Interjet', 'Mexico'),
    ('SouthWest', 'EEUU'),
    ('American Airlines', 'EEUU'),
    ('Delta Air Lines', 'EEUU'),
    ('United Continental Holdings', 'EEUU'),
    ('Lufthansa', 'Alemania'),
    ('Air France', 'Francia'),
    ('International Airlines', 'España'),
    ('China Southern Airlines', 'China'),
    ('China Eastern Airlines', 'China'),
    ('All Nippon Airways', 'Japon'),
    ('Ryanair', 'India'),
    ('Air China', 'China'),
    ('Emirates', 'Emirator Arabes Unidos'),
    ('British Airways', 'Reino Unido'),
    ('Garuda Indonesia', 'Indonesia'),
    ('Swiss International Air Lines', 'Suiza'),
    ('Air New Zealand', 'Nueva Zelanda'),
    ('Bangkok Airways', 'Tailandia'),
    ('KLM Royal Dutch Airlines', 'Paises Bajos'),
    ('AirAsia', 'Malasia'), 
    ('Virgin Atlantic', 'Reino Unido'), 
    ('Aeroflot', 'Rusia'),
    ('Hong Kong Airlines', 'China'),
    ('Virgin Australia', 'Australia'),
    ('Turkish Airlines', 'Turquia'),
    ('Asiana Airlines', 'Corea del Sur'),
    ('Etihad Airways', 'Emiratos Arabes Unidos'),
    ('Air Canada', 'Canada'),
    ('Azul Airlines', 'Brasil'),
    ('Avianca', 'Colombia'),
    ('TAP Portugal', 'Portugal'),
    ('Copa Airlines', 'Colombia'),
    ('Aeromexico', 'Mexico'),
    ('Volaris', 'Mexico'),
    ('LATAM', 'Chile'),
    ('EcoJet', 'Bolivia'),
    ('Avianca Ecuador', 'Ecuador'),
    ('Air Italy', 'Italia');
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_airplane_data():
    query = \
    """
    INSERT INTO Airplane (Enrollment, Clasif, Capacity, No_Tripulante) VALUES
    ('N12345', 'Comercial', 8, 2), 
    ('N1234a', 'Comercial', 19, 4), 
    ('B1234', 'Comercial', 10, 3),
    ('N123ab', 'Comercial', 15, 3),
    ('N123a', 'Comercial', 19, 4),
    ('CSabc', 'Comercial', 10, 2),
    ('N1a', 'Comercial', 20, 4),
    ('B012345','Carga',100, 5), 
    ('HK123HJ','Comercial', 100, 4),
    ('F-OG54ab','Comercial', 29, 3),
    ('EC-23001','Carga', 180, 5),
    ('EC-78AA0','Carga', 200, 8),
    ('G95abcd', 'Comercial', 45, 5),
    ('N82312a', 'Carga', 80, 4),
    ('N57212','Comercial', 65, 4),
    ('N73912ab','Comercial', 90, 4),
    ('N62941', 'Comercial', 65, 3),
    ('N6941ab', 'Carga', 30, 3),
    ('N49291a','Carga', 1100, 7),
    ('N5612ab', 'Militar', 78, 4),
    ('N3123ab', 'Carga', 48, 3),
    ('CU-T1240', 'Comercial', 15, 2),
    ('CU-T1547', 'Comercial', 20, 2),
    ('CU-T1548', 'Comercial', 30, 2),
    ('CU-T1710', 'Comercial', 40, 2),
    ('CU-T1711', 'Comercial', 40, 2),
    ('CU-T1712', 'Comercial', 40, 2),
    ('CU-T1713', 'Comercial', 40, 2),
    ('CU-T1714', 'Comercial', 40, 2),
    ('CU-T1715', 'Comercial', 40, 2),
    ('CU-T1716', 'Comercial', 40, 2),
    ('N468251a', 'Comercial', 29, 2),
    ('LVBARC', 'Comercial', 23, 3),
    ('EC-AA0', 'Comercial', 37, 3),
    ('EC-ZZ9', 'Comercial', 48, 3),
    ('HK5838', 'Comercial', 23, 3),
    ('HK4728', 'Comercial', 14, 2)
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_total_passenger_data():
    query = """
    INSERT INTO Total_Passenger (Clasif, Capacity, No_Tripulante, Total_Passenger) VALUES
    ('Comercial', 10, 2, 8),
    ('Comercial', 20, 4, 16),
    ('Carga',100, 5, 95), 
    ('Comercial', 100, 4, 46),
    ('Comercial', 29, 3, 26),
    ('Carga', 180, 5, 175),
    ('Carga', 200, 8, 192),
    ('Comercial', 45, 5, 40),
    ('Carga', 80, 4, 76),
    ('Comercial', 65, 4, 61),
    ('Comercial', 90, 4, 86),
    ('Comercial', 65, 3, 62),
    ('Carga', 30, 3, 27),
    ('Carga', 1100, 7, 143),
    ('Militar', 78, 4, 74),
    ('Carga', 48, 3, 45),
    ('Comercial', 15, 2, 13),
    ('Comercial', 20, 2, 18),
    ('Comercial', 30, 2, 28),
    ('Comercial', 40, 2, 38),
    ('Comercial', 29, 2, 27),
    ('Comercial', 37, 3, 34),
    ('Comercial', 48, 3, 45),
    ('Comercial', 23, 3, 20),
    ('Comercial', 14, 2, 12);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_client_data():
    query = \
    """
    INSERT INTO Client (Name_C, Last_name_C, Country_C, ID_Telegram_C, No_Passport) VALUES
    ('Sheila', 'Artiles Fagundo', 'Espanna', 372768, 37596),
    ('Gustavo', 'Despaigne Dita', 'Australia', 6780131, 28445),
    ('Grettel', 'Hernandez Garbey', 'Francia', 990903, 833673),
    ('Jennifer Lynn', 'Lopez', 'EEUU', 57291, 73792),
    ('Edward Christopher', 'Sheeran', 'Gran Bretanna', 902993, 21002),
    ('Cristiano Ronaldo', 'dos Santos Aveiro', 'Portugal', 20383, 18455),
    ('Heydi', 'Despaigne Dita', 'Cuban', 33833, 117618),
    ('Marco Antonio', 'Munniz Rivera', 'Puerto Rico', 447209, 39933),
    ('Thomas', 'Cruise Mapother IV', 'EEUU', 990999, 339303),
    ('Keith', 'Rupert Murdoch', 'EEUU', 5798, 66779),
    ('Carolina', 'Giraldo Navarro', 'Colombia', 282810, 67439),
    ('Danna Paola', 'Rivera Munguia', 'Mexico', 24474, 29922),
    ('Sebastian', 'Yatra', 'Colombia', 929231, 3120308),
    ('Martina', 'Stoessel', 'Argentina', 449202, 199910),
    ('Bryan', 'Machin Gracia', 'Cuba', 663932, 11191),
    ('Carolina', 'Herrera Garcia', 'Mexico', 777837, 300101),
    ('Maria Fernanda', 'Zamora', 'Ecuador', 667575, 288390),
    ('Silenayd', 'LLerena Lopez', 'Sudafrica', 83720, 19922),
    ('Pedro', 'Chapotin', 'Puerto Rico', 283994, 190299),
    ('Victor Manuel', 'Maceo Mendez', 'Angola', 28405, 100019),
    ('Abraham Mateo', 'Chamorro', 'Espanna', 395553, 44449),
    ('Edgar Ricardo', 'Arjona Morales', 'Guatemala', 4011029, 94832),
    ('Samuel Frederick', 'Smith', 'Gran Bretana', 832923, 382099),
    ('Demetria Devonne', 'Lovato', 'EEUU', 564745, 383494),
    ('Harry Edward', 'Styles', 'Gran Bretanna', 58210, 93891),
    ('Karla Camila', 'Cabello Estrabao', 'Cuba', 900019, 40192),
    ('Adam', 'Levine', 'EEUU', 37104, 28469),
    ('Alessia', 'Caracciolo', 'Canada', 865568, 45203),
    ('Shawn Peter Raul', 'Mendes', 'Canada', 46556, 89284),
    ('Peter Gene', 'Hernandez', 'EEUU', 999054, 35795),
    ('Luis Alfonso', 'Rodriguez Lopez-Cepero', 'Puerto Rico', 38793, 209328),
    ('Ramon', 'Melendi Espina', 'Espanna', 668125, 94324),
    ('Lionel Andres', 'Messi Cuccittini', 'Argentina', 120054, 48456),
    ('Maximiliano Teodoro', 'Iglesias Acevedo', 'Espanna', 99909, 445920),
    ('José Antonio', 'Dominguez Bandera', 'Espanna', 774790, 339548),
    ('Juan Luis', 'Londonno Arias ', 'Colombia', '864368', 34452), 
    ('Kimberly Noel', 'Kardashian West', 'EEUU', '554534', 111112),
    ('John Joseph', 'Travolta', 'EEUU', '26443', 222925), 
    ('Amancio', 'Ortega Gaona', 'Espanna', '23456', 889928)
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_flight_data():
    query = \
    """
    INSERT INTO Flight(ID_A, Cod_F, Aeroport_S, Date_Hour_S, Aeroport_L, Date_Hour_L, Price) VALUES
    (1, 16093, 4, '2021-06-03 06:30', 10, '2021-06-03 07:30', 4366),
    (2, 15503, 14, '2021-06-03 18:00', 11, '2021-06-03 19:00', 231),
    (3, 27334, 5, '2021-06-03 06:00', 9, '2021-06-03 09:00', 3234),
    (4, 93944, 12, '2021-06-03 19:00', 7, '2021-06-03 21:00', 1134),
    (5, 94954, 21, '2021-06-03 22:15', 26, '2021-06-03 1:00', 134),
    (6, 34744, 29, '2021-06-03 5:00', 22, '2021-06-03 10:00', 134),
    (7, 28224, 8, '2021-06-03 18:00', 23, '2021-06-03 21:00', 6432),
    (8, 49555, 21, '2021-07-05 1:00', 22, '2021-07-05 2:30', 654), 
    (9, 88938, 10, '2021-06-01 05:00', 12, '2021-05-30 06:00', 754),
    (10, 10019, 30, '2021-06-01 01:30', 10, '2021-05-30 04:00', 434),
    (3, 99889, 10, '2021-06-01 01:30', 22, '2021-05-30 02:30', 3545),
    (2, 1234, 10, '2021-06-03 9:30', 6, '2021-06-03 11:30', 3545),
    (2, 1534, 10, '2020-06-03 9:30', 1, '2021-06-03 11:30', 3545);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_bookingto_data():
    query = \
    """
    INSERT INTO BookingTo(ID_B, ID_C) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 18),
    (2, 2),
    (2, 3),
    (3, 3),
    (3, 21),
    (8, 8),
    (8, 9),
    (8, 11),
    (8, 31),
    (8, 30),
    (13, 13),
    (13, 16),
    (13, 27), 
    (14, 1);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_booking_data():
    query = \
    """
    INSERT INTO Booking (ID_C, ID_F, Date_booking, IS_paid) VALUES
    (1, 3, '2021-12-08 9:00', 0),
    (14, 3, '2021-11-07 4:30', 0),
    (15, 3, '2021-04-09 11:30', 0),
    (22, 1, '2021-08-18 1:00', 0),
    (2, 9, '2021-10-01 12:15', 0),
    (3, 10, '2021-10-01 8:30', 0),
    (8, 5, '2021-05-01 5:00', 0),
    (19, 7, '2021-02-01 7:00', 0),
    (11, 1, '2021-04-09 12:00', 0),
    (23, 1, '2021-10-09 1:00', 0),
    (28, 4, '2021-07-27 3:00', 0),
    (22, 4, '2021-08-04 11:00', 0),
    (33, 2, '2021-09-02 5:45', 0), 
    (1, 13, '2021-05-29 01:30', 1);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_buy_data():
    query = \
    """
    INSERT INTO Buy (Date_Buy) VALUES
    ('2020-07-04'),
    ('2020-05-03'),
    ('2019-09-05'),
    ('2020-05-24'),
    ('2009-03-13'),
    ('2020-04-02 12:05'),
    ('2019-04-09'),
    ('2020-03-19'),
    ('2020-03-05'),
    ('2019-09-05'),
    ('2009-07-16'),
    ('2009-07-16'), 
    ('2020-08-09 12:15'),
    ('2020-08-09 12:15'),
    ('2020-08-09 12:15'),
    ('2019-05-05 10:15'),
    ('2019-05-05 10:15'),
    ('2019-05-05 10:15'),
    ('2018-04-25 10:15'),
    ('2018-04-25 10:15'),
    ('2018-04-25 10:15'),
    ('2014-01-01 11:15'),
    ('2017-06-02 11:15'),
    ('2017-06-02 11:15'), 
    ('2021-02-14 11:30');
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
def insert_product_data():
    query = \
    """
    INSERT INTO Product (Name_Prod, Cost_Prod) VALUES
    ('Big Mac', 10),
    ('Pizza de Sartén', 15),
    ('Alitas de Pollo', 13),
    ('Hamburguesa', 8),
    ('Pizza de Pepperoni', 15),
    ('Chocolate caliente', 20),
    ('Capuchino', 3),
    ('Ray-Ban', 70),
    ('Brindan variedades de zapatos deportivos Adidas', 70),
    ('Calzado Converse All Star color negro', 60),
    ('Brindan variedades de zapatos deportivos NB', 70),
    ('Pantalón vaquero', 25),
    ('Playera', 4),
    ('Samsung Galaxy S9', 500),
    ('iPhone 20', 1200);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_repair_data():
    query = \
    """
    INSERT INTO Repair (Cod_R, Type_R, Cost_R) VALUES
    (251, 'Accesorios', 100),
    (256, 'Accesorios',80),
    (231, 'Accesorios', 50),
    (211, 'Accesorios', 45),
    (232, 'Accesorios', 78),
    (255, 'Accesorios', 110),
    (230, 'Accesorios', 90),
    (202, 'Accesorios', 65),
    (246, 'Accesorios', 90),
    (203, 'Accesorios', 180),
    (262, 'Accesorios', 100),
    (240, 'Accesorios', 10),
    (233, 'Autopropulsión', 250),
    (215, 'Autopropulsión', 200),
    (242, 'Autopropulsión', 350),
    (206, 'Autopropulsión', 100),
    (214, 'Autopropulsión', 500),
    (213, 'Autopropulsión', 200),
    (235, 'Carpintería de metal', 2500),
    (221, 'Carpintería de metal', 2000),
    (236, 'Carpintería de metal', 4000),
    (222, 'Carpintería de metal', 2000),
    (258, 'Carpintería de metal', 2000),
    (204, 'Carpintería de metal', 2000),
    (260, 'Carpintería de metal', 1600),
    (238, 'Carpintería de metal', 1780),
    (212, 'Carpintería de metal', 900),
    (254, 'Carpintería de metal', 5000),
    (229, 'Carpintería de metal', 2500),
    (227, 'Carpintería de metal', 1900),
    (252, 'Carpintería de metal', 1070),
    (208, 'Carpintería de metal', 1500),
    (207, 'Carpintería de metal', 1500),
    (247, 'Carpintería de metal', 2000),
    (209, 'Carpintería de metal', 1700),
    (210, 'Carpintería de metal', 1000),
    (234, 'Carpintería de metal', 1500),
    (263, 'Electricidad', 75),
    (253, 'Electricidad', 75),
    (228, 'Electricidad', 75),
    (241, 'Electricidad', 75),
    (205, 'Electricidad', 75),
    (248, 'Capital', 100),
    (245, 'Capital', 100),
    (218, 'Capital', 100),
    (219, 'Capital', 100),
    (265, 'Capital', 100),
    (249, 'Capital', 100),
    (216, 'Capital', 100),
    (243, 'Capital', 100),
    (244, 'Capital', 100),
    (217, 'Capital', 100),
    (220, 'Capital', 100),
    (224, 'Capital', 100),
    (225, 'Capital', 100),
    (257, 'Capital', 100),
    (226, 'Capital', 100),
    (2100, 'Capital', 100),
    (266, 'Capital', 100),
    (264, 'Capital', 100),
    (259, 'Limpieza', 50),
    (237, 'Limpieza', 50),
    (223, 'Limpieza', 50);     
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_need_repair_data():
    query = \
    """
    INSERT INTO Need_Repair (Cod_R, Cod_R1) VALUES
    (248, 246),
    (218, 221),
    (218, 222),
    (216, 215),
    (216, 213),
    (243, 242),
    (217, 213),
    (217, 214),
    (224, 225),
    (225, 224),
    (266, 263),
    (220, 221),
    (220, 223);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_date_data():
    query = \
    """
    INSERT INTO Date (Date_Begin) VALUES
    ('2007-01-01'), 
    ('2008-01-01'), 
    ('2010-03-01'),
    ('2014-09-14'),
    ('2014-01-01'),
    ('2007-05-01'),
    ('2018-06-13'),
    ('2020-03-01'),
    ('2019-04-04'),
    ('2020-08-09'),
    ('2018-04-25'),
    ('2017-06-02'),
    ('2015-02-14'),
    ('2013-03-23'),
    ('2016-02-08'),
    ('2006-04-04'),
    ('2007-09-07'),
    ('2009-07-15'),
    ('2019-05-05'), 
    ('2015-05-05'),
    ('2018-08-19'),
    ('2018-07-26'),
    ('2014-04-23'),
    ('2006-06-28'),
    ('2009-07-16'),
    ('2020-07-04'),
    ('2020-05-03'),
    ('2019-09-05'),
    ('2020-05-24'),
    ('2009-03-13'),
    ('2020-04-02'),
    ('2019-04-09'),
    ('2020-03-19'),
    ('2020-03-05'),
    ('2020-08-09 02:30'),
    ('2020-08-09 12:15'),
    ('2019-05-05 10:15'),
    ('2019-05-05 02:30'),
    ('2018-04-25 10:15'), 
    ('2018-04-25 02:30'),
    ('2014-01-01 11:15'),
    ('2014-01-01 19:30'),
    ('2017-06-02 11:15'), 
    ('2017-06-02 19:30'),
    ('2015-02-14 11:30'), 
    ('2015-02-14 19:45'),
    ('2013-03-23 11:30'),
    ('2013-03-23 19:45'),
    ('2014-04-23 11:30'), 
    ('2014-04-23 19:45'), 
    ('2016-02-08 08:30'), 
    ('2016-02-08 10:45'), 
    ('2006-04-04 08:30'), 
    ('2006-04-04 10:45'),
    ('2007-01-01 08:30'), 
    ('2007-01-01 10:45'),
    ('2007-09-07 09:30'), 
    ('2007-09-07 12:45'),
    ('2009-07-15 09:30'), 
    ('2009-07-15 12:45'),
    ('2015-05-05 09:30'), 
    ('2015-05-05  12:45'),
    ('2007-01-14'),  
    ('2008-02-14'), 
    ('2010-03-02'), 
    ('2014-01-14'),
    ('2007-05-07'), 
    ('2018-06-21'),
    ('2006-07-02'),
    ('2010-05-02'),
    ('2020-07-02'),
    ('2018-08-20'),
    ('2019-04-07'),
    ('2018-08-01'),
    ('2020-07-14'),
    ('2020-05-05'),
    ('2020-05-30'),
    ('2009-05-05'),
    ('2020-04-02 12:05'), 
    ('2020-04-02 22:15'),
    ('2019-04-10'),
    ('2020-03-22'),
    ('2020-03-25'),
    ('2019-09-10'),
    ('2009-08-16'),
    ('2009-07-20'),
    ('2007-01-15'),
    ('2008-02-14 12:05'),
    ('2010-03-01 23:15'),
    ('2014-09-14 23:45'),
    ('2014-01-15'),
    ('2007-05-06 22:30'),
    ('2007-01-12'),
    ('2007-01-16'),
    ('2018-06-25'),
    ('2010-05-01 23:40'),
    ('2020-07-01'),
    ('2019-04-08'),
    ('2020-08-09 10:25'),
    ('2018-04-25 10:30'),
    ('2014-01-01 11:40'),
    ('2017-06-02 11:30'),
    ('2015-02-14 11:40'),
    ('2013-03-23 11:40'),
    ('2016-02-08 08:40'),
    ('2006-04-04 08:40'),
    ('2007-09-07 09:40'),
    ('2007-01-01 08:45'),
    ('2009-07-15 09:45'),
    ('2015-05-05 09:40'),
    ('2018-08-19 00:10'),
    ('2018-07-26 00:15'),
    ('2014-04-23 11:38'),
    ('2006-06-28 00:20'),
    ('2009-07-16 00:05'), 
    ('2010-07-16 00:20');
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_Apply_Repair():
    query = \
    """
    INSERT INTO Apply_Repair(Enrollment, Cod_R, Date_Begin, Date_End, Time, ID_AeroP, ID_I) VALUES
    ('N12345', 223, '2007-01-01', '2007-01-14', 50, 10, 1), 
    ('N12345', 220, '2008-01-01', '2008-02-14', 93, 10, 2),
    ('N1234a', 241, '2010-03-01', '2010-03-02', 3, 3, 4),
    ('B1234',  223, '2014-09-14', '2014-09-14', 1, 2, 3),
    ('N123ab', 230, '2014-01-01', '2014-01-14', 50, 7, 5),
    ('N123ab', 242, '2007-05-01', '2007-05-07', 16, 2, 6),
    ('CSabc',  225, '2007-01-01', '2007-01-14', 50, 2, 6), 
    ('CU-T1240', 225, '2007-01-01', '2007-01-14', 50, 1, 7),
    ('CU-T1547', 223, '2018-06-13', '2018-06-21', 20, 5, 8),
    ('CU-T1548', 242, '2010-03-01', '2010-05-02', 100, 3, 4),
    ('CU-T1710', 223, '2020-03-01', '2020-07-02', 190, 1, 7),
    ('CU-T1711', 230, '2019-04-04', '2019-04-07', 9, 18, 9);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_product_installation_data():
    query = \
    """
    INSERT INTO Product_Installation (ID_AeroP, ID_I, ID_Prod, Count_Prod) VALUES
    (17, 10, 1, 85),
    (5, 8, 2, 35),
    (17, 10, 3, 15),
    (3, 4, 4, 72),
    (3, 4, 5, 75),
    (5, 8, 6, 70),
    (18, 9, 7, 45),
    (5, 8, 8, 25),
    (17, 10, 9, 150),
    (10, 18, 10, 40),
    (10, 18, 11, 20),
    (18, 9, 12, 11),
    (2, 3, 13, 34),
    (2, 3, 14, 100),
    (3, 4, 15, 25);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_employee_data():
    query = \
    """
    INSERT INTO Employee (Name_E, Last_name_E, Country_NE, ID_Telegram_E, Cod_Verif, Job, DNI, ID_AeroP, ID_I) VALUES
    ('Blanca R',                'Victores Gutierrez',   'Cuba',         85190,      \'\',       'Empleado de Instalacion',              58513093007, \'17\', 10),
    ('Haydee E',	            'Castillo Victores',	'Francia',	    30925,	    \'\',       'Empleado de Puerta de Salida',	        29445834107, \'1\', NULL),
    ('Michel',                  'Castro Glez',          'Cuba',	        74325,	    \'\',	    'Empleado de Mostrador',                38931402937, \'3\', NULL),
    ('Nancy',                   'Sotolongo García',     'Cuba',	        3667,	    \'\',	    'Empleado de Mostrador',                58140649865, \'5\', NULL),
    ('Ivonne',	                'Súarez Roche',	        'Cuba',	        22923,	    \'\',	    'Gerente de ventas',                    55595349654, \'6\', NULL),
    ('Lisbet',	                'Ricardo Pupo',         'Cuba',	        44239,	    \'\',	    'Empleado de Puerta de Salida',	        57704877085, \'3\', NULL),
    ('Emilia',	                'Fdez Mtnez',	        'Cuba',	        34922,	    \'\',	    'Empleado de Puerta de Salida',         38363866426, \'8\', NULL),
    ('Luis Manuel',	            'Hdez Fdez',	        'Cuba',	        62028,	    \'\',	    'Empleado de Puerta de Salida',         86678952466, \'3\', NULL),
    ('Mirian C',	            'Torres Chaviano',	    'España',	    41613,	    \'\',	    'Operador de Vuelo',                    66501918968, \'9\', NULL),
    ('Juana L',                 'Martin Ruiz',	        'Cuba',	        27831,	    \'\',	    'Operador de Vuelo',                    94640388211, \'2\', NULL),
    ('Raquel',	                'Liriano Azahares',	    'Cuba',	        23446,	    \'\',	    'Empleado de Mostrador',                78747288970, \'1\', NULL),
    ('Orlando',	                'Sierra Liriano',	    'Cuba',	        62995,	    \'\',	    'Empleado de Mostrador',                80348355613, \'5\', NULL),
    ('Raquel',	                'Sierra Liriano',	    'Cuba',	        8963,	    \'\',	    'Operador de Vuelo',                    60458174076, \'10\',NULL ),
    ('Aitana',	                'Cabrera Sierra',	    'Cuba',	        5296,	    \'\',	    'Empleado de Mostrador',                42904456096, \'4\', NULL),
    ('Inés',	                'Carnet Quiala',	    'Cuba',	        23826,	    \'\',	    'Empleado de Mostrador',                10013730675, \'9\', NULL),
    ('Mercedes de La Caridad',	'Mora Carnet',	        'Cuba',	        13080,	    \'\',	    'Empleado de Recursos Humanos',	        61677608095, \'3\', NULL),
    ('Marlen',	                'Rojas Angulo',	        'Mexico',	    41148,	    \'\',	    'Operador de Vuelo',                    57112871018, \'1\', NULL),
    ('Yadisbel',	            'Morejon Rojas',	    'Brasil',	    51403,	    \'\',	    'Operador de Vuelo',                    54423106000, \'6\', NULL),
    ('Ana Nida',	            'Nacer Martí',	        'Argentina',	51231,	    \'\',	    'Empleado de Recursos Humanos',	        67354345297, \'4\', NULL),
    ('María de Jesús',	        'Valdés Pérez',	        'Puerto Rico',	89587,	    \'\',	    'Empleado de Instalacion',              79940673430, \'2\', 3),
    ('Diana',	                'Bernes Díaz',	        'Cuba',	        62151,	    \'\',	    'Empleado de Mostrador',                59037998006, \'8\', NULL),
    ('Rene',	                'Gutierrez Díaz',	    'Cuba',	        12716,	    \'\',	    'Empleado de Instalacion',	            52304804382, \'17\', 10),
    ('Irma',	                'Marrero Súarez',	    'Cuba',	        12591,	    \'\',	    'Jefe de Mecanica',                     47060466972, \'2\', NULL),
    ('Susana',	                'Illana De Mier',	    'Cuba',	        27003,	    \'\',	    'Empleado de Recursos Humanos',         40105145266, \'19\', NULL),
    ('Miguel',	                'Rguez Marrero',	    'Cuba',	        11434,	    \'\',	    'Empleado de Mostrador',                44236609916, \'11\', NULL),
    ('Sandra',	                'Marrero Illana',	    'Cuba',	        34208,	    \'\',	    'Empleado de Mostrador',                56567755028, \'12\', NULL),
    ('Juan A.',	                'Sosa Hdez',	        'Cuba',	        2280,	    \'\',	    'Empleado de Mostrador',                87311724601, \'18\', NULL),
    ('Juan R',	                'Zulueta Vilches',	    'Cuba',	        65305,	    \'\',	    'Jefe de Supervisor de Instalaciones',	93601960083, \'3\', 4),
    ('Emérida V',	            'Quintana Sánchez',	    'Cuba',	        31374,	    \'\',	    'Empleado de Mostrador',                87431575838, \'17\', NULL),
    ('Justo O',	                'Iriterán Quintana',	'Cuba',	        92742,	    \'\',	    'Empleado de Mostrador',                81703021539, \'17\', NULL),
    ('Pavel',	                'Carvajal Pérez',       'Mexico',	    26691,	    \'\',	    'Empleado de Mostrador',                52338347438, \'10\', NULL),
    ('Mireya',	                'Hdez Taboada',	        'Cuba',	        55571,	    \'\',	    'Empleado de Mostrador',	            67750492027, \'13\', NULL),
    ('Niurka',	                'Perdomo Hdez',	        'Cuba',	        85451,	    \'\',	    'Jefe de Almacen',	                    98617838107, \'17\', 10),
    ('Maritza',                 'Aguero García',	    'Cuba',	        10399,	    \'\',	    'Empleado de Recursos Humanos',         87396100279, \'20\', NULL),
    ('Osiel',	                'Fdez Navarro',	        'Mexico',	    38188,	    \'\',	    'Empleado de Mostrador',                69395107729, \'9\', NULL),
    ('Teresa',	                'Súarez Gálvez',	    'Mexico',	    89131,	    \'\',	    'Empleado de Instalacion',              39885295897, \'2\', 3),
    ('Roman',	                'Mario Valdés',	        'Mexico',	    85869,	    \'\',	    'Empleado de Instalacion',              50497404989, \'17\', 10),
    ('Jorge',                   'Carnot Pereira',	    'Panama',       30538,      \'\',	    'Empleado de Mostrador',                53790877336, \'1\', NULL),
    ('GDD',                     'MC',                   'Cuba',         716780131, \'\',       'employee_humanResources',             99, 10, 18),
    ('Sheila',                     'MC',                   'Cuba',         937372768, \'\',       'employee_flightOperator',             99, 10, 18);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_aeroline_matric_data():
    query = \
    """
    INSERT INTO Aeroline_Matric (Enrollment, ID_A) VALUES
    ('B012345', 8), 
    ('HK123HJ', 14),
    ('F-OG54ab', 29),
    ('EC-23001', 10),
    ('EC-78AA0', 17),
    ('G95abcd', 9),
    ('N82312a', 4),
    ('N57212', 24),
    ('N73912ab',4 ),
    ('N62941', 5),
    ('N6941ab', 15),
    ('N49291a', 7),
    ('N5612ab', 4),
    ('N3123ab', 25),
    ('CU-T1240', 26),
    ('CU-T1547', 26),
    ('CU-T1548', 26),
    ('CU-T1710', 26),
    ('CU-T1711', 26),
    ('CU-T1712', 26),
    ('CU-T1713', 26),
    ('CU-T1714', 26),
    ('CU-T1715', 26),   
    ('CU-T1716', 26);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_client_matric_data():
    query = \
    """
    INSERT INTO Client_Matric (Enrollment, ID_C) VALUES
    ('N12345', 12), 
    ('N1234a', 11), 
    ('B1234',10),
    ('N123ab', 9),
    ('N123a', 8),
    ('CSabc', 5),
    ('N1a', 3);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_flight_matric_data():
    query = \
    """
    INSERT INTO Flight_Matric (Enrollment, ID_F) VALUES
    ('B012345', 8), 
    ('HK123HJ', 7),
    ('F-OG54ab', 2),
    ('EC-23001', 10),
    ('EC-78AA0', 1),
    ('G95abcd', 9),
    ('N82312a', 6),
    ('N57212', 3),
    ('N73912ab',4),
    ('N62941', 5),
    ('N62941', 12);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_passenger_flow_data():
    query =\
    """
    INSERT INTO Passenger_Flow (ID_C, ID_F, isAccepted_S, isAccepted_E) VALUES
    (3, 1, 1, NULL),
    (4, 1, 0, NULL),
    (18, 1, 0, NULL),
    (1, 8, 0, NULL),
    (14, 1, 1, NULL),
    (15, 1, 1, 0),
    (13, 1,1, 1),
    (20, 1, 1, 1),
    (22, 9, 0, NULL),
    (23, 9, 1, 1),
    (2, 4, 1, 0),
    (3, 4, 1, 1),
    (3, 3, 1, 1),
    (21, 3, 0, NULL),
    (8, 2, 1, NULL),
    (9, 2, 1, 0),
    (11, 2, 1, 1),
    (31, 2, 1, 0),
    (30, 2, 1, 1),
    (19, 2, 0, NULL),
    (14, 2, 0, NULL),
    (19, 6, 1, 1),
    (11, 8, 1, 0),
    (11, 9, 0 , NULL),
    (23, 5, 0, NULL),
    (4, 5, 1, 1),
    (27, 5, 1, 1),
    (8, 5, 1, 1),
    (28, 6, 1, 0),
    (23, 6, 0, 1),
    (38, 6, 1, 1),
    (22, 6, 1, 0),
    (33, 8, 1, NULL),
    (5, 8, 0, NULL),
    (34, 8, 0, NULL),
    (3, 8, 1, 1),
    (2, 8, 1, 0),
    (9, 8, 1, 1)
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_airfare_data():
    query = \
    """
    INSERT INTO Airfare(ID_C, ID_F, Count_Baggage) VALUES
    (1, 12, NULL),
    (2, 12, NULL),
    (3, 1, 2),
    (4, 1, 1),
    (18, 1, 1),
    (1, 8, 2),
    (14, 1, 2),
    (15, 1, 2),
    (13, 1, 1),
    (20, 1, 3),
    (22, 9, 5),
    (23, 9, 3),
    (2, 4, 1),
    (3, 4, 2),
    (3, 3, 2),
    (21, 3, 2),
    (8, 2, 3),
    (9, 2, 3),
    (11, 2, 2),
    (31, 2, 1),
    (30, 2, 2),
    (19, 2, 1),
    (14, 2, 2),
    (19, 6, 5),
    (11, 8, 1),
    (11, 9, 2),
    (23, 5, 3),
    (4, 5, 2),
    (27, 5, 1),
    (8, 5, 1),
    (28, 6, 2),
    (23, 6, 2),
    (38, 6, 3),
    (22, 6, 1),
    (33, 8, 2),
    (5, 8, 2),
    (34, 8, 3),
    (3, 8, 1),
    (2, 8, 2),
    (9, 8, 2),
    (13, 10, 1),
    (16, 10, 2),
    (27, 10, 2)
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_product_buy_data():
    query = \
    """
    INSERT INTO Product_Buy(ID_Prod, ID_Buy, Count_Prod, ID_I, ID_AeroP) VALUES
    (1, 1, 3, 29, 21),
    (1, 2, 2, 26, 18),
    (13, 1, 1, 26, 18),
    (4, 2, 10, 14, 30),
    (4, 7, 1, 13, 2),
    (9, 8, 14, 21, 29),
    (8, 3, 5, 20, 1),
    (11, 17, 9, 19, 25),
    (8, 5, 2, 17, 13),
    (6, 6, 11, 16, 23),
    (3, 7, 10, 14, 30),
    (5, 2, 9, 13, 2),
    (3, 19, 2, 12, 9),
    (5, 3, 11, 10, 17);
    """
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(query)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_job():
    sql = """INSERT INTO Office(Office, Salary)
            VALUES(%s,%s)"""
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, ("Gerente de Ventas", 256))
        cur.execute(sql, ("Empleado de Mostrador", 24.8))
        cur.execute(sql, ("Empleado de Migracion", 2344))
        cur.execute(sql, ("Empleado de Puerta de Salida", 445.8))
        cur.execute(sql, ("Operador de Vuelo", 3545))
        cur.execute(sql, ("Empleado de Recursos Humanos", 765))
        cur.execute(sql, ("Jefe de Mecanica", 7634))
        cur.execute(sql, ("Jefe de Almacen", 4657))
        cur.execute(sql, ("Jefe de Supervisor de Instalaciones", 4543.8))
        cur.execute(sql, ("Empleado de Instalacion", 4543.8))
        
        # commit the changes to the database 
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_all_data():
    insert_aeroport_data()
    insert_InstallationType_data()
    insert_installation_data()
    insert_aeroline_data()
    insert_airplane_data()
    insert_total_passenger_data()
    insert_client_data()
    insert_flight_data()
    insert_booking_data()
    insert_bookingto_data()
    insert_buy_data()
    insert_product_data()
    insert_repair_data()
    insert_need_repair_data()
    insert_date_data()
    insert_product_installation_data()
    insert_employee_data()
    insert_aeroline_matric_data()
    insert_client_matric_data()
    insert_flight_matric_data()
    insert_passenger_flow_data()
    insert_airfare_data()
    insert_product_buy_data()
    insert_job()
    insert_Apply_Repair()
