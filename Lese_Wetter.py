import WS980_Weather
import MySqlDB_Weather
import locale

from MySqlDB_Weather import Weather_Johan211_DB
from WS980_Weather import Station_Request

locale.setlocale(locale.LC_ALL, "de_DE")
locale.setlocale(locale.LC_NUMERIC, "de_DE")

# Abfrage der Wetterstation
WerteAkt = bytes(b'\xff\xff\x0b\x00\x06\x04\x04\x19')
IP = '192.168.100.135'
req: Station_Request = WS980_Weather.Station_Request(WerteAkt, IP)
# print(req.recv_data)

AlleWerte = WS980_Weather.leseWerteVektor(req.recv_data)

print(AlleWerte)

# Speichern der Werte in der mysql Datenbank

AnzWerte = len(AlleWerte) + 5  # 5 freie Plätze
Host = "localhost"  # Lokal auf Z440
# Host = "192.168.100.8"   # NAS3
Port = "3306"
# Port = "3307"            # Nas3
Weather: Weather_Johan211_DB = MySqlDB_Weather.Weather_Johan211_DB(AnzWerte, Host, Port)
# Weather.Drop_Table()
Weather.Create_Table()
Weather.INSERT_Table(AlleWerte)

# Abfrage aus DB
Weather.SELECT_Table(1, 5)
print(Weather.myresult)

Weather.Export_Csv()
