import paho.mqtt.client as mqtt
import time
import threading
from time import sleep
import random

from screen import Screen
from controls import Controls

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.connect("172.17.0.1", 1883, 60)

# Define how large the world should be
WORLD_SIZE_X = 64
WORLD_SIZE_Y = 64

screen = Screen(WORLD_SIZE_X, WORLD_SIZE_Y)
controls = Controls()

player_position = (1, 1)

zombies = [(5, 2), (3, 5), (2, 7)]

def handle_up(is_pressed):
    global player_position
    player_position = (player_position[0], max(1, (player_position[1] - 1)))
    screen.set_player_position(player_position)

def handle_down(is_pressed):
    global player_position
    player_position = (player_position[0], min((WORLD_SIZE_Y - 1), (player_position[1] + 1)))
    screen.set_player_position(player_position)

def handle_left(is_pressed):
    global player_position
    player_position = (max(1, (player_position[0] - 1)), player_position[1])
    screen.set_player_position(player_position)

def handle_right(is_pressed):
    global player_position
    player_position = (min((player_position[0] + 1), WORLD_SIZE_X - 1), player_position[1])
    screen.set_player_position(player_position)

def do_tick():
    global zombies
    while True:

        new_zombies = []
        zombie_index = random.randint(0, len(zombies) - 1)
        zombie = zombies[zombie_index]

        new_x = zombie[0]
        new_y = zombie[1]
        if (zombie[0] > player_position[0]):
            new_x -= 1

        if (zombie[0] < player_position[0]):
            new_x += 1

        if (zombie[1] > player_position[1]):
            new_y -= 1

        if (zombie[1] < player_position[1]):
            new_y += 1

        new_zombie = (new_x, new_y)
        zombies[zombie_index] = new_zombie

        screen.set_zombies(zombies)
        sleep(1)

def main():
    print("Hello world")

    controls.start(handle_up, handle_down, handle_left, handle_right)
    screen.start()

    # Put zombies
    screen.set_zombies(zombies)

    # Run tick
    tickThread = threading.Thread(
        target=do_tick, daemon=True
    )
    tickThread.start()

    try:
        while True:
            time.sleep(1)  # Schläft ressourcenschonend für 1 Sekunde und wiederholt
    except KeyboardInterrupt:
        print("\nProgramm wird sauber beendet...")

if __name__ == "__main__":
    main()

print("End")
