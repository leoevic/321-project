import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

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

from game import Game

# Define how large the world should be
WORLD_SIZE_X = 12
WORLD_SIZE_Y = 12

def main():
    Game(WORLD_SIZE_X, WORLD_SIZE_Y)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExit")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

print("End")
