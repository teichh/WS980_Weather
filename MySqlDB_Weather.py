import mysql.connector
import os

import db_config
from db_config import DB_PORT


# Generiere String fuer Create und Update Werte1 bis N
def SQLWerte_Table(anz: object) -> object:
    Spaltenname = Spaltennamen_create("Wert", anz)
    AlleSpalten = ", ".join(Spaltenname)
    CreateAlleSpalten = " REAL,".join(Spaltenname) + " REAL"
    # print(AlleSpalten)
    # print(CreateAlleSpalten)
    return CreateAlleSpalten, AlleSpalten


# Spaltennamen erzeugen
def Spaltennamen_create(Namex: str, anz: int):
    Spaltenname = []
    for n in range(1, anz + 1):
        Spaltenname.append(Namex + str(n))
    # print(Spaltenname)
    return Spaltenname


class Weather_Johan211_DB():
    def __init__(self, Anzwerte: object) -> object:
        self.mydb = mysql.connector.connect(
            host=db_config.HOST,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            database=db_config.DB_NAME,
            port=db_config.DB_PORT
        )
        self.AnzWerte = Anzwerte
        self.my_cursor = self.mydb.cursor()
        self.CreateAlleSpalten, self.AlleSpalten = SQLWerte_Table(self.AnzWerte)

    # SQL_CREATE_TABLE = 'CREATE TABLE Messungen (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))'

    def Create_Table(self):
        CreateSql1: str = """
                            CREATE TABLE IF NOT EXISTS Messungen
                            (id INT AUTO_INCREMENT PRIMARY KEY, 
                            Zeit TIMESTAMP,
                            AlleSpalten 
                            )
                            """
        CreateSql1 = CreateSql1.replace("AlleSpalten", self.CreateAlleSpalten)

        # CreateValues: tuple = ('Wert1 REAL', 'Wert2 REAL')
        # print(CreateSql1 % CreateValues)
        # print(CreateSql1 % CreateValues)
        self.my_cursor.execute(CreateSql1)
        # self.my_cursor.execute("CREATE TABLE IF NOT EXISTS Messungen "
        #                       "(id INT AUTO_INCREMENT PRIMARY KEY, "
        #                       "Zeit TIMESTAMP, "
        #                       "Wert1 REAL) "
        #                       )

        # self.my_cursor.execute("CREATE TABLE IF NOT EXISTS Messungen (id INT AUTO_INCREMENT PRIMARY KEY, Zeit DATE, typ INT, Wert REAL,

    def Alter_Table(self):
        self.my_cursor = self.mydb.cursor()
        self.my_cursor.execute("ALTER TABLE Messungen "
                               "ADD Wert2 REAL "
                               )
        add_column = "ALTER TABLE Messungen  ADD Wert3 REAL"
        self.my_cursor.execute(add_column)

    def Drop_Table(self):
        self.my_cursor = self.mydb.cursor()
        self.my_cursor.execute("DROP TABLE IF EXISTS Messungen")

    def INSERT_Table(self, Werte: float):
        self.my_cursor = self.mydb.cursor()
        InsertSql = """
                    INSERT INTO Messungen 
                    (Zeit AlleSpalten) 
                    VALUES ( 
                    NOW() 
                    AlleWerte
                    );
                    """
        InsertSpalten = ""
        InsertValue = ""
        Spalte: object
        for Spalte in (Werte.keys()):
            InsertSpalten = InsertSpalten + ", " + Spalte
            InsertValue = InsertValue + ", " + str(Werte[Spalte])

        InsertSql = InsertSql.replace("AlleSpalten", InsertSpalten)
        InsertSql = InsertSql.replace("AlleWerte", InsertValue)

        self.my_cursor.execute(InsertSql)
        # self.my_cursor.execute("INSERT INTO Messungen (Zeit, Wert1, Wert2) VALUES (NOW(), 11.1, 22.1)")
        self.mydb.commit()

        print('Fertig')

    def Export_Csv(self):
        self.my_cursor = self.mydb.cursor()

        Outfile = "C:/Users/Thomas/Downloads/weather.csv"
        if os.path.exists(Outfile): os.remove(Outfile)

        CsvSql = """
                SELECT * FROM Messungen 
                INTO OUTFILE 'C:/Users/Thomas/Downloads/weather.csv'
                FIELDS ENCLOSED BY '"' 
                TERMINATED BY ';'
                ESCAPED BY '"'
                LINES TERMINATED BY '\n';
                """
        self.my_cursor.execute(CsvSql)
#
#       Dezimalpunkt durch Komma ersetzen
#
        f1 = open(Outfile, "r")
        CsvFile = "C:/Users/Thomas/Downloads/weather1.csv"
        f2 = open(CsvFile,"w")
        for line in f1:
            f2.write(line.replace(".", ","))
        f1.close()
        f2.close ()


    # Lese N Messungen aus Spalte X
    def SELECT_Table(self, Index, anz: int):
        self.my_cursor = self.mydb.cursor()
        # SelectSql = "SELECT Wert" + str(Index) + " FROM Messungen LIMIT "+str(anz)
        # SelectSql = "SELECT Zeit,Wert" + str(Index) + " FROM Messungen ORDER BY Zeit DESC LIMIT "+str(anz)
        SelectSql = 'SELECT DATE_FORMAT(Zeit, \'%d.%m.%Y %H:%i:%s\') AS Zeit ,Wert' + str(
            Index) + ' FROM Messungen ORDER BY Zeit DESC LIMIT ' + str(anz)
        self.my_cursor.execute(SelectSql)

        self.myresult = self.my_cursor.fetchall()

        print('Select: Fertig')

#Weather = Weather_Johan211_DB(20)

# Weather.Drop_Table()
# Weather.Create_Table()
# Weather.Alter_Table()

# Werte: float = (11.1 ,11.1 ,11.1 ,11.1 ,11.1 ,11.1 ,11.1 ,11.1 ,11.1 ,11.1)
# Weather.INSERT_Table(Werte)

# my_cursor = Weather.mydb.cursor()
# my_cursor.execute("CREATE DATABASE WeatherJohan211")
# my_cursor.execute("SHOW DATABASES")

#Weather.Export_Csv()
