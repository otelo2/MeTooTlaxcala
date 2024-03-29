import psycopg2
import psycopg2.extras
import json
from dbKeys import DB_HOST, DB_NAME, DB_USER, DB_PASS

class DatabaseConnector:
#Constructor
    def __init__(self):
        #conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        a=1
        #conn.close()

#Creates the database table schema
    def createTable(self):
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

#Adds data to the database table
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

#Adds the contents from the tweets.txt file to the databse
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
                    #The [1:] is to remove the first space
                    self.addToTable(nombre, apellidoPaterno[1:], apellidoMaterno[1:], denuncia[1:], imagen1[1:], imagen2[1:], imagen3[1:], imagen4[1:], fecha, hora, link[1:], tweetID[1:])
                    #Print the person who was just added
                    if verbose:
                        print(f"{index+1}: Added person {nombre} {apellidoPaterno[1:]} {apellidoMaterno[1:]}.")
            if verbose:
                print(f"Added {index+1} entries to the database")
        except FileNotFoundError:
            print("File not found error")

#Adds specific contents from the tweets.txt file to the databse
    def specificTweetsFileToDatabase(self, verbose=True, amount=1000):
        try:
            with open("tweets.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                print(f"amount = {amount}")
                for index, line in enumerate(lines[::-1]):
                    #Adds just the lines specified in the amount paramenter
                    if int(index) == int(amount):
                        print("Breaking now")
                        break
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
                    #The [1:] is to remove the first space
                    self.addToTable(nombre, apellidoPaterno[1:], apellidoMaterno[1:], denuncia[1:], imagen1[1:], imagen2[1:], imagen3[1:], imagen4[1:], fecha, hora, link[1:], tweetID[1:])
                    #Print the person who was just added
                    if verbose:
                        print(f"{index+1}: Added person {nombre} {apellidoPaterno[1:]} {apellidoMaterno[1:]}.")
            if verbose:
                print(f"Added {index} entries to the database")
        except FileNotFoundError:
            print("File not found error")

#Perform the query in the argument
    def databaseToJSON(self):
        #Connect to the database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        with conn:
            #Create the cursor. Result is in a dictionary
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                #id | nombre | apellidoPaterno | apellidoMaterno | denuncia | imagen1 | imagen2 | imagen3 | imagen4 | fecha | hora | link | tweetID
                #Performs the query to put into a json file the contents of the database
                cur.execute("SELECT * FROM abusador;")

                #Write the output to file
                with open("Frontend/data/abusador.json", "w", encoding="utf-8") as f:
                    f.write(str(json.dumps(cur.fetchall(), indent=4, sort_keys=False, default=str)))
                    print("Wrote file to /Frontend/data/abusador.json")