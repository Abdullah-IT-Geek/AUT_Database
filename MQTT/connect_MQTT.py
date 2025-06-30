import paho.mqtt.client as mqtt
from tinydb import TinyDB
import json
import os
import time


script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "../config.json")
# 🔹 Config laden
try:
    with open(config_path, "r") as f:
        file_content = f.read()
        print("[DEBUG] config.json Inhalt:", file_content)
        config = json.loads(file_content)
except FileNotFoundError:
    print("[ERROR] Die config.json Datei wurde nicht gefunden.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"[ERROR] config.json konnte nicht gelesen werden. JSONDecodeError: {e}")
    exit(1)
except Exception as e:
    print(f"[ERROR] Unerwarteter Fehler beim Laden der config.json: {e}")
    exit(1)

#Extrahieren vpn der config - datei
broker = config["broker"]
port = config["port"]
topic = config["topic"]
username = config["username"]
password = config["password"]


# Datenbank initialisieren
db = TinyDB("mqtt_data.json")

3
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code != 0:
        print(f"[ERROR] Verbindung fehlgeschlagen: {reason_code}")
    else:
        print("Verbunden mit Broker.")
        client.subscribe(topic, qos=1)


def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"[ERROR] MQTT Verbindung getrennt. Reason Code: {reason_code}")

    # Automatisch reconnecten mit Backoff
    while True:
        try:
            print("[INFO] Versuche Reconnect...")
            client.reconnect()
            print("[INFO] Reconnect erfolgreich.")
            break
        except Exception as e:
            print(f"[ERROR] Reconnect fehlgeschlagen: {e}")
            time.sleep(5)
            
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
        print("[ERROR] Ungültiger JSON-String.")

def on_subscribe(client, userdata, mid, reason_code_list, properties=None):
    if reason_code_list and reason_code_list[0].is_failure:
        print(f"Subscription abgelehnt: {reason_code_list[0]}")
    else:
        print(f"Subscribed. QoS: {reason_code_list[0].value}")

# MQTT Client erstellen
mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
mqttc.username_pw_set(username, password)

mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

mqttc.connect(broker, port)
mqttc.loop_forever()
