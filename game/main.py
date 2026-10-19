import paho.mqtt.client as mqtt
import time
import threading
from time import sleep
import random

"""
 _______________________________
| I am the magic cow that hates |
| AI-generated code             |
 -------------------------------
        |   ^__^
        |___(oo)________
            (__)        )---
                ||----w |
                ||     ||
"""

from screen import Screen
from controls import Controls
from game import Game

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect("172.17.0.1", 1883, 60)

# Define how large the world should be
WORLD_SIZE_X = 12
WORLD_SIZE_Y = 12

def main():
    Game(WORLD_SIZE_X, WORLD_SIZE_Y)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgramm wird sauber beendet...")

if __name__ == "__main__":
    main()

print("End")
