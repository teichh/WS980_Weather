import locale
import db_config

import MySqlDB_Weather
import WS980_Weather
from MySqlDB_Weather import Weather_Johan211_DB
from WS980_Weather import Station_Request

locale.setlocale(locale.LC_ALL, "de_DE.utf8")
locale.setlocale(locale.LC_NUMERIC, "de_DE.utf8")

# Abfrage der Wetterstation
WerteAkt = bytes(b'\xff\xff\x0b\x00\x06\x04\x04\x19')

req: Station_Request = WS980_Weather.Station_Request(WerteAkt, db_config.ws980_ip)
# print(req.recv_data)

AlleWerte = WS980_Weather.leseWerteVektor(req.recv_data)

print(AlleWerte)

# Speichern der Werte in der mysql Datenbank

AnzWerte = len(AlleWerte) + 5  # 5 freie Plätze

Weather: Weather_Johan211_DB = MySqlDB_Weather.Weather_Johan211_DB(AnzWerte)
# Weather.Drop_Table()
Weather.Create_Table()
Weather.INSERT_Table(AlleWerte)

# Abfrage aus DB
Weather.SELECT_Table(1, 5)
print(Weather.myresult)

Weather.Export_Csv()
