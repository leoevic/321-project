import paho.mqtt.client as mqtt
import time

from screen import Screen
from controls import Controls

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect("172.17.0.1", 1883, 60)

screen = Screen()
controls = Controls()

player_position = (0, 0)

def handle_up(is_pressed):
    global player_position
    player_position = (player_position[0], (player_position[1] - 1) % 8)
    screen.set_player_position(player_position)

def handle_down(is_pressed):
    global player_position
    player_position = (player_position[0], (player_position[1] + 1) % 8)
    screen.set_player_position(player_position)

def handle_left(is_pressed):
    global player_position
    player_position = ((player_position[0] - 1) % 8, player_position[1])
    screen.set_player_position(player_position)

def handle_right(is_pressed):
    global player_position
    player_position = ((player_position[0] + 1) % 8, player_position[1])
    screen.set_player_position(player_position)

def main():
    print("Hello world")

    controls.start(handle_up, handle_down, handle_left, handle_right)
    screen.start()

    try:
        while True:
            time.sleep(1)  # Schläft ressourcenschonend für 1 Sekunde und wiederholt
    except KeyboardInterrupt:
        print("\nProgramm wird sauber beendet...")

if __name__ == "__main__":
    main()

print("End")
