import paho.mqtt.client as mqtt
from screen import Screen

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect("172.17.0.1", 1883, 60)

screen = Screen()