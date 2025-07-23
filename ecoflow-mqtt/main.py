import time
import requests
import json
import paho.mqtt.client as mqtt

ECOFLOW_IP = "192.168.1.185"
SERIAL = "your_serial_here"
TOKEN = "your_token_here"

MQTT_BROKER = "mqtt://homeassistant"
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "ecoflow/delta3plus"

def get_data():
    url = f"http://{ECOFLOW_IP}/api/devices/{SERIAL}/status"
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    response = requests.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()

def publish_to_mqtt(data):
    client = mqtt.Client()
    client.connect("homeassistant", MQTT_PORT, 60)

    payload = {
        "soc": data.get("soc"),
        "input_power": data.get("input_power"),
        "output_power": data.get("output_power")
    }

    client.publish(f"{MQTT_TOPIC_PREFIX}/status", json.dumps(payload))
    client.disconnect()

while True:
    try:
        data = get_data()
        publish_to_mqtt(data)
    except Exception as e:
        print("Error:", e)
    time.sleep(1)
