import paho.mqtt.client as mqtt
from tinydb import TinyDB
import json

# Konfiguration
broker = "158.180.44.197"
port = 1883
topic = "iot1/teaching_factory/#"

# Datenbank initialisieren
db = TinyDB("mqtt_data.json")

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        print(f"❌ Verbindung fehlgeschlagen: {reason_code}")
    else:
        print("✅ Verbunden mit Broker.")
        client.subscribe(topic, qos=1)

def on_message(client, userdata, message):
    payload_raw = message.payload.decode('utf-8').strip()
    topic_parts = message.topic.split('/')
    table_name = topic_parts[-1] if topic_parts else "unknown"

    print(f"Topic: {message.topic}")
    print(f"Tabellenname: {table_name}")
    print(f"Payload: {payload_raw}")

    try:
        # Versuche Payload als JSON zu laden
        data = json.loads(payload_raw)
        if isinstance(data, dict):
            db.table(table_name).insert(data)
            print(f"Gespeichert in Tabelle '{table_name}': {data}")
        else:
            print("JSON muss ein Objekt ({}-Struktur) sein.")
    except json.JSONDecodeError:
        print(" Fehler: Ungültiger JSON-String.")

def on_subscribe(client, userdata, mid, reason_code_list, properties=None):
    if reason_code_list and reason_code_list[0].is_failure:
        print(f"Subscription abgelehnt: {reason_code_list[0]}")
    else:
        print(f"Subscribed. QoS: {reason_code_list[0].value}")

# MQTT Client erstellen
mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set("bobm", "letmein")

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe

mqttc.connect(broker, port)
mqttc.loop_forever()
