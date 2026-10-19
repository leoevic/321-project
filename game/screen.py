import re
import time
import threading
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class Screen:
    def __init__(self, world_x, world_y):
        self.player_position = (1, 1)
        self.zombies = []

        self.fireballs = []

        self.world_x = world_x
        self.world_y = world_y

        self.world_border_a = (0, 0)
        self.world_border_b = (world_x, 0)
        self.world_border_c = (0, world_y)
        self.world_border_d = (world_x, world_y)

        self.camera_position = (0, 0)

        self.serial = spi(port=0, device=1, gpio=noop())
        self.device = max7219(self.serial, cascaded=1, block_orientation=90, rotate=0)
        self.device.clear()

        self.even_frame = False

        # Draw one dot
        with canvas(self.device) as draw:
            draw.rectangle(self.device.bounding_box, fill="black")
            draw.point((3, 3), fill="white")
            draw.point((4, 3), fill="white")
            draw.point((5, 3), fill="white")
            draw.point((6, 3), fill="white")

    def start(self):
        # Start thread
        drawThread = threading.Thread(
            target=self.draw, daemon=True
        )
        drawThread.start()

    def reset_camera(self):
        self.camera_position = (0, 0)

    def set_player_position(self, pos: tuple):
        self.player_position = pos

        new_camera_position_x = self.camera_position[0]
        new_camera_position_y = self.camera_position[1]

        # Correct camera position x
        if (self.player_position[0] >= 0 and self.player_position[0] <= self.world_x):
            if (self.player_position[0] - self.camera_position[0] == 7):
                new_camera_position_x += 1
            elif (self.camera_position[0] == self.player_position[0]):
                new_camera_position_x -= 1

        # Correct camera position y
        if (self.player_position[1] >= 0 and self.player_position[1] <= self.world_y):
            if (self.player_position[1] - self.camera_position[1] == 7):
                new_camera_position_y += 1
            elif (self.camera_position[1] == self.player_position[1]):
                new_camera_position_y -= 1

        self.camera_position = (new_camera_position_x, new_camera_position_y)

    def determine_screen_position(self, pos: tuple):
        return (pos[0] - self.camera_position[0], pos[1] - self.camera_position[1])

    def set_zombies(self, zombies: list):
        self.zombies = zombies

    def set_fireballs(self, fireballs: list):
        self.fireballs = fireballs

    def draw(self):
        while True:
            with canvas(self.device) as draw:
                # Clear screen
                draw.rectangle(self.device.bounding_box, fill="black")

                # We want an even frame because some things should not be shown in every frame
                self.even_frame = not self.even_frame

                # Draw world border
                top_left = self.determine_screen_position(self.world_border_a)
                bottom_right = self.determine_screen_position(self.world_border_d)
                draw.rectangle((top_left[0], top_left[1], bottom_right[0], bottom_right[1]), outline="white", fill="black")

                # Draw player position
                draw.point(self.determine_screen_position(self.player_position), fill="white")

                # Draw zombies
                for zombie in self.zombies:
                    draw.point(self.determine_screen_position(zombie), fill="white")

                # Draw fireballs
                if self.even_frame:
                    for fireball in self.fireballs:
                        draw.point(self.determine_screen_position((fireball[0], fireball[1])), fill="white")

            time.sleep(1 / 30)

