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
fireball_orientation = "right"

zombies = [(5, 2), (3, 5), (2, 7)]

fireballs = []

# We need a lock to avoid race condition between fireballs and zombies
data_lock = threading.Lock()

def handle_up(is_pressed):
    global player_position
    global fireball_orientation
    player_position = (player_position[0], max(1, (player_position[1] - 1)))
    fireball_orientation = "up"
    screen.set_player_position(player_position)

def handle_down(is_pressed):
    global player_position
    global fireball_orientation
    player_position = (player_position[0], min((WORLD_SIZE_Y - 1), (player_position[1] + 1)))
    fireball_orientation = "down"
    screen.set_player_position(player_position)

def handle_left(is_pressed):
    global player_position
    global fireball_orientation
    player_position = (max(1, (player_position[0] - 1)), player_position[1])
    fireball_orientation = "left"
    screen.set_player_position(player_position)

def handle_right(is_pressed):
    global player_position
    global fireball_orientation
    player_position = (min((player_position[0] + 1), WORLD_SIZE_X - 1), player_position[1])
    fireball_orientation = "right"
    screen.set_player_position(player_position)

def handle_shoot(is_pressed):
    global fireballs
    new_fireball = (player_position[0], player_position[1], fireball_orientation)
    fireballs.append(new_fireball)

def do_zombie_tick():
    global zombies
    while True:

        if not zombies:
            sleep(1)
            pass

        with data_lock:

            # Get random zombie
            if zombies:
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

def do_fireball_tick():
    global fireballs
    global zombies
    while True:

        with data_lock:

            new_fireballs = []

            for fireball in fireballs:
                new_x = fireball[0]
                new_y = fireball[1]
                direction = fireball[2]

                if direction == "up":
                    new_y -= 1
                elif direction == "down":
                    new_y += 1
                elif direction == "left":
                    new_x -= 2
                elif direction == "right":
                    new_x += 1

                # Destroy zombies
                zombies = list(filter(lambda z: z[0] != new_x or z[1] != new_y, zombies))

                if 0 <= new_x <= WORLD_SIZE_X and 0 <= new_y <= WORLD_SIZE_Y:
                    new_fireballs.append((new_x, new_y, direction))

            fireballs = new_fireballs
            screen.set_fireballs(fireballs)
        sleep(1 / 2)

def main():
    print("Hello world")

    controls.start(handle_up, handle_down, handle_left, handle_right, handle_shoot)
    screen.start()

    # Put zombies
    screen.set_zombies(zombies)

    # Put fireballs (the screen doesnt know the difference between zombies and fireballs)
    screen.set_fireballs(fireballs)

    # Run tick
    zombieTickThread = threading.Thread(
        target=do_zombie_tick, daemon=True
    )
    zombieTickThread.start()

    fireballTickThread = threading.Thread(
        target=do_fireball_tick, daemon=True
    )
    fireballTickThread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgramm wird sauber beendet...")

if __name__ == "__main__":
    main()

print("End")
