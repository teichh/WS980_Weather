import socket

Sensor_Index =  [ 6, 9, 12, 15, 18, 21, 23, 25, 28, 31, 34, 37, 40, 45, 50, 55, 60, 65, 70, 75, 78]
Sensor_Laenge = [ 2, 2,  2,  2,  2,  1,  1,  2,  2,  2,  2,  2,  4,  4,  4,  4,  4,  4,  4,  2,  1]
Sensor_scale =  [10,10, 10, 10, 10,  1,  1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
Sensor_Dim = ['°C', '°C', '°C', '°C', '°C',
              '%', '%',
              'hPa', 'hPa',
              'Grad',
              'm/s', 'm/s',
              'mm', 'mm', 'mm', 'mm', 'mm', 'mm',
              'lux', 'uW/m2', 'UvIdxRaw', 1]
Sensor_Typ = ['Wert Innentemperatur      in 0.1 °C',
              'Wert Außentemperatur      in 0.1 °C',
              'Wert Temperatur Taupunkt  in 0.1 °C',
              'Wert gefühlte Temperatur  in 0.1 °C',
              'Wert  Temp. Hitzeindex    in 0.1 °C',
              'Wert Innenfeuchte         in %',
              'Wert Aussenfeuchte        in %',
              'Wert = abs. Druck         in 1/10 hPa',
              'Wert rel. Druck  in hPa',
              'Wert Windrichtung in Grad',
              'Wert Windgeschw in 1/10 m/s',
              'Wert Windbö in m/s',
              'Wert Regen/h in 0.1 mm',
              'Wert Regen/d in 0.1 mm',
              'Wert Regen/w in 0.1 mm',
              'Wert Regen/Monat in 0.1 mm',
              'Wert Regen/Jahr in 0.1 mm',
              'Wert Regen gesamt in 0.1 mm',
              'Wert Licht in 0.1 lux',
              'Wert UvRaw in 1 uW/m2',
              'Wert UvIdxRaw']

# Lese Mehrbyte-Wert aus Bytefeld
def shiftWert(value, ix1, len1, scale):
    result = 0
    for ix in range(len1):
        result1 = value[ix+ix1+1]
        result = result*256 + result1
# für negative Werte
    if result > 2**(len1*8-1):
        result = 2**(len1*8) - result
        result = - result

    return result / scale

def leseWerteVektor(bytefeld:object) -> object:
    """

    :type bytefeld: object
    """
    WerteListe = {}
    for x in range(len(Sensor_Index)):
        ix = Sensor_Index[x]
        typ = bytefeld[ix]
        len1 = Sensor_Laenge[x]
        scale = Sensor_scale[x]
        Wert = shiftWert(bytefeld, ix, len1, scale)
        Dim = Sensor_Dim[x]
        print ('Sensor=', Sensor_Typ[x], 'Index=', ix ,'len=',len1 ,'Wert=',Wert, Dim)
        WertTyp = 'Wert' + str(typ)
        WerteListe[WertTyp] = Wert
    #print (Sensor_Index)
    #print (Sensor_Laenge)
    return WerteListe

class Station_Request():
    def __init__(self, abfrage,IP) -> object:
        self.TCP_IP = IP
        self.TCP_PORT = 45000
        self.BUFFER_SIZE = 1024
        self.message = abfrage

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.TCP_IP, self.TCP_PORT))
        s.send(self.message)
        self.recv_data: bytes = s.recv(self.BUFFER_SIZE)
        s.close()
        #print('Antwort: %d' , s.recv)

WerteAkt = bytes(b'\xff\xff\x0b\x00\x06\x04\x04\x19')
WerteMax = bytes(b'\xff\xff\x0b\x00\x06\x05\x05\x1b')
WerteMin = bytes(b'\xff\xff\x0b\x00\x06\x06\x06\x1d')
WerteTagmax = bytes(b'\xff\xff\x0b\x00\x06\x07\x07\x1f')
