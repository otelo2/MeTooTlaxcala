import psycopg2
import psycopg2.extras
from dbKeys import DB_HOST, DB_NAME, DB_USER, DB_PASS

class DatabaseConnector:
    #Constructor
    def __init__(self):
        #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        a=1
        #conn.close()

    #Creates the database table schema
    def createTable():
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha 
                # | hora | link | tweetID
                #Just creates the table.
                cur.execute("CREATE TABLE abusador (id SERIAL PRIMARY KEY, nombre VARCHAR, apellidoPaterno VARCHAR, \
                            apellidoMaterno VARCHAR, denuncia VARCHAR, imagen1 VARCHAR, imagen2 VARCHAR, imagen3 VARCHAR, \
                            imagen4 VARCHAR, fecha DATE, hora TIME, link VARCHAR, tweetID VARCHAR);")

#Drops the database table schema
    def dropTable():
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha 
                # | hora | link | tweetID
                #Just creates the table.
                cur.execute("DROP TABLE abusador;")

    def addToTable(nombre, apellidoPaterno, apellidoMaterno, denuncia, imagen1, imagen2, imagen3, imagen4, fecha, hora, link, tweetID):
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha | hora | link | tweetID
                #Just creates the table.
                query = f"INSERT INTO abusador VALUES(DEFAULT, '{nombre}', '{apellidoPaterno}', '{apellidoMaterno}', '{denuncia}', \
                    '{imagen1}', '{imagen2}', '{imagen3}', '{imagen4}', '{fecha}', '{hora}', '{link}', '{tweetID}');"
                cur.execute(query)

    def testQueryINSERT():
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha | hora | link | tweetID
                #Prints all the contents from the abusador table
                nombre = "Santiago"
                apellidoPaterno = "Yael"
                apellidoMaterno = "Pérez"
                denuncia = "Denuncia contra Santiago Yael Pérez V #MeToo #YoSiTeCreo #NoEstasSola https://t.co/KizyjRauSI"
                imagen1 = "/img/SantiagoYaelPérez--Ehn.jpg"
                imagen2 = "/img/SantiagoYaelPérez--5Ff.jpg"
                imagen3 = "/img/SantiagoYaelPérez--umu.jpg"
                imagen4 = "/img/SantiagoYaelPérez--ZFO.jpg"
                fecha = "2021-03-26"
                hora = "03:38:39"
                link = "https://twitter.com/twitter/statuses/1375291080170741760"
                tweetID = "1375291080170741760"
                query = f"INSERT INTO abusador VALUES(DEFAULT, '{nombre}', '{apellidoPaterno}', '{apellidoMaterno}', '{denuncia}', \
                    '{imagen1}', '{imagen2}', '{imagen3}', '{imagen4}', '{fecha}', '{hora}', '{link}', '{tweetID}');"
                cur.execute(query)

    def testQuerySELECT():
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha | hora | link | tweetID
                #Prints all the contents from the abusador table
                cur.execute("SELECT * FROM abusador;")
                print(cur.fetchall())

    #Perform the query in the argument
    def customQuery(query):
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha | hora | link | tweetID
                #Performs a custom query
                cur.execute(str(query))
                print(cur.fetchall())

    #Adds the contents from thw tweets.txt file to the databse
    def tweetsFileToDatabase(self, verbose=True):
        try:
            with open("tweets.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                for index, line in enumerate(lines):
                    #Create a list of the relevant data
                    line = line.split(",")
                    #Put data into variables for verbosity
                    nombre = line[0]
                    apellidoPaterno = line[1]
                    apellidoMaterno = line[2]
                    denuncia = line[3]
                    imagen1 = line[4]
                    imagen2 = line[5]
                    imagen3 = line[6]
                    imagen4 = line[7]
                    fecha = line[8]
                    hora = line[9]
                    link = line[10]
                    tweetID = line[11]
                    #Place the data in the database
                    self.addToTable(nombre, apellidoPaterno, apellidoMaterno, denuncia, imagen1, imagen2, imagen3, imagen4, fecha, hora, link, tweetID)
                    #Print the person who was just added
                    if verbose:
                        print(f"{index+1}: Added person {nombre} {apellidoPaterno} {apellidoMaterno}.")
            if verbose:
                print(f"Added {index+1} entries to the database")
        except FileNotFoundError:
            print("File not found error")
