import json
import paho.mqtt.client as mqtt

# MQTT-Client erzeugen
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# MQTT-Anmeldung
mqtt_client.username_pw_set(
    username="mqttuser",
    password="geheim"
)

# Verbindung herstellen
mqtt_client.connect(
    host="192.168.100.211",
    port=1883,
    keepalive=60
)

SENSORS = [
    ("Wert1",  "Innentemperatur",      "temperature", "°C"),
    ("Wert2",  "Außentemperatur",      "temperature", "°C"),
    ("Wert3",  "Taupunkt",             "temperature", "°C"),
    ("Wert4",  "Gefühlte Temperatur",  "temperature", "°C"),
    ("Wert5",  "Hitzeindex",           "temperature", "°C"),
    ("Wert6",  "Innenfeuchte",         "humidity",    "%"),
    ("Wert7",  "Außenfeuchte",         "humidity",    "%"),
    ("Wert8",  "Absoluter Druck",      "pressure",    "hPa"),
    ("Wert9",  "Relativer Druck",      "pressure",    "hPa"),
    ("Wert10", "Windrichtung",         None,          "°"),
    ("Wert11", "Windgeschwindigkeit",  None,          "m/s"),
    ("Wert12", "Windböen",             None,          "m/s"),
    ("Wert13", "Regen Stunde",         None,          "mm"),
    ("Wert14", "Regen Tag",            None,          "mm"),
    ("Wert15", "Regen Woche",          None,          "mm"),
    ("Wert16", "Regen Monat",          None,          "mm"),
    ("Wert17", "Regen Jahr",           None,          "mm"),
    ("Wert18", "Regen Gesamt",         None,          "mm"),
    ("Wert19", "Helligkeit",           "illuminance", "lux"),
    ("Wert20", "UV Raw",               None,          "µW/m²"),
    ("Wert21", "UV Index",             None,          "")
]

for feld, name, devclass, unit in SENSORS:

    config = {
        "name": name,
        "unique_id": f"ws980_{feld.lower()}",
        "state_topic": f"ws980/{feld}",
        "unit_of_measurement": unit,
        "state_class": "measurement",
        "device": {
            "identifiers": ["ws980"],
            "name": "WS980",
            "manufacturer": "ELV",
            "model": "WS980"
        }
    }

    if devclass:
        config["device_class"] = devclass

    mqtt_client.publish(
        f"homeassistant/sensor/ws980/{feld.lower()}/config",
        json.dumps(config),
        retain=True
    )

    for feld, _, _, _ in SENSORS:
        mqtt_client.publish(
            f"ws980/{feld}",
            0,
            retain=True
        )

# Aktuelle Werte veröffentlichen
def MQTT_Werte(Allewerte):
    for feld, _, _, _ in SENSORS:

        wert = Allewerte.get(feld)
        if wert is None:
            continue
        if wert == "":
            continue

        mqtt_client.publish(
            f"ws980/{feld}",
            str(wert),
            retain=True
        )
    return
