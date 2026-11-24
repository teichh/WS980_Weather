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

sensors = [
    ("Wert1", "Temperatur Wohnzimmer", "temperature", "°C"),
    ("Wert2", "Temperatur Außen", "temperature", "°C"),
    ("Wert3", "Luftfeuchte Wohnzimmer", "humidity", "%"),
    ("Wert4", "Luftdruck", "pressure", "hPa"),
]

for wert, name, device_class, unit in sensors:

    config = {
        "name": name,
        "unique_id": f"ws980_{wert.lower()}",
        "state_topic": f"ws980/{wert}",
        "device_class": device_class,
        "state_class": "measurement",
        "unit_of_measurement": unit,
        "device": {
            "identifiers": ["ws980"],
            "name": "WS980",
            "manufacturer": "ELV",
            "model": "WS980"
        }
    }

    mqtt_client.publish(
        f"homeassistant/sensor/ws980/{wert.lower()}/config",
        json.dumps(config),
        retain=True
    )