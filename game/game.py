import threading
import time
import random

from screen import Screen
from controls import Controls

class Game:
    def __init__(self, world_x, world_y):
        self.screen = Screen(world_x, world_y)
        self.controls = Controls()

        self.screen.start()
        self.controls.start(self.handle_up, self.handle_down, self.handle_left, self.handle_right, self.handle_shoot)

        self.running = False

        self.player_position = (1, 1)
        self.fireball_orientation = "right"
        self.score = 0

        self.zombies = [(5, 2), (3, 5), (2, 7)]
        self.fireballs = []

        self.world_x = world_x
        self.world_y = world_y

        self.data_lock = threading.Lock()

        # Prepare threads
        self.zombieTickThread = None
        self.fireballTickThread = None

        self.zombieTickSignal = threading.Event()
        self.fireballTickSignal = threading.Event()

    """
    Reset game data
    """
    def reset_game_data(self):
        self.running = False
        self.player_position = (1, 1)
        self.fireball_orientation = "right"
        self.score = 0

        self.screen.reset_camera()
        self.screen.set_player_position(self.player_position)

        # Clear signals
        self.zombieTickSignal.clear()
        self.fireballTickSignal.clear()

        self.zombieTickThread = threading.Thread(
            target=self.do_zombie_tick, daemon=True, args=(self.zombieTickSignal,)
        )
        self.fireballTickThread = threading.Thread(
            target=self.do_fireball_tick, daemon=True, args=(self.fireballTickSignal,)
        )

        self.zombies = [(5, 2), (3, 5), (2, 7)]
        self.fireballs = []

    """
    Start game
    """
    def start(self):
        self.reset_game_data()
        self.running = True

        self.zombieTickThread.start()
        self.fireballTickThread.start()

    def stop(self):
        self.running = False

        self.zombieTickSignal.set()
        self.fireballTickSignal.set()

    """
    Handle the up key
    """
    def handle_up(self, is_pressed):
        if self.running:
            self.player_position = (self.player_position[0], max(1, (self.player_position[1] - 1)))
            self.fireball_orientation = "up"
            self.screen.set_player_position(self.player_position)

    """
    Handle the down key
    """
    def handle_down(self, is_pressed):
        if self.running:
            self.player_position = (self.player_position[0], min((self.world_y - 1), (self.player_position[1] + 1)))
            self.fireball_orientation = "down"
            self.screen.set_player_position(self.player_position)

    """
    Handle the left key
    """
    def handle_left(self, is_pressed):
        if self.running:
            self.player_position = (max(1, (self.player_position[0] - 1)), self.player_position[1])
            self.fireball_orientation = "left"
            self.screen.set_player_position(self.player_position)

    """
    Handle the right key
    """
    def handle_right(self, is_pressed):
        if self.running:
            self.player_position = (min((self.player_position[0] + 1), self.world_x - 1), self.player_position[1])
            self.fireball_orientation = "right"
            self.screen.set_player_position(self.player_position)

    """
    Handle the shoot key
    """
    def handle_shoot(self, is_pressed):
        if not self.running:
            self.start()
        else:
            self.new_fireball = (self.player_position[0], self.player_position[1], self.fireball_orientation)
            self.fireballs.append(self.new_fireball)

    """
    Handle the movement of the zombies once a second. Tick, tock, tick, tock
    """
    def do_zombie_tick(self, stop_event):
        while True:

            if not self.zombies:
                time.sleep(1)
                pass

            with self.data_lock:

                # Get random zombie
                if self.zombies:
                    zombie_index = random.randint(0, len(self.zombies) - 1)

                    zombie = self.zombies[zombie_index]

                    new_x = zombie[0]
                    new_y = zombie[1]
                    if (zombie[0] > self.player_position[0]):
                        new_x -= 1

                    if (zombie[0] < self.player_position[0]):
                        new_x += 1

                    if (zombie[1] > self.player_position[1]):
                        new_y -= 1

                    if (zombie[1] < self.player_position[1]):
                        new_y += 1

                    new_zombie = (new_x, new_y)
                    self.zombies[zombie_index] = new_zombie

                    # Game over if a zombie has eaten the player
                    if new_zombie[0] == self.player_position[0] and new_zombie[1] == self.player_position[1]:
                        self.stop()

                    self.screen.set_zombies(self.zombies)

            if (stop_event.wait(timeout=1.0)):
                break

    """
    Do fireball tick twice a second, tick tock tick tock, but a little faster
    """
    def do_fireball_tick(self, stop_event):
        while True:

            with self.data_lock:

                new_fireballs = []

                for fireball in self.fireballs:
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
                    old_length = len(self.zombies)
                    self.zombies = list(filter(lambda z: z[0] != new_x or z[1] != new_y, self.zombies))
                    new_length = len(self.zombies)

                    if (old_length > new_length):
                        self.score += 1

                    if 0 <= new_x <= self.world_x and 0 <= new_y <= self.world_y:
                        new_fireballs.append((new_x, new_y, direction))

                self.fireballs = new_fireballs
                self.screen.set_fireballs(self.fireballs)
            
            if (stop_event.wait(timeout=0.5)):
                break
