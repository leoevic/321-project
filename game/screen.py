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
    def __init__(self):
        self.player_position = (0, 0)

        self.serial = spi(port=0, device=1, gpio=noop())
        self.device = max7219(self.serial, cascaded=1, block_orientation=90, rotate=0)
        self.device.clear()

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

    def set_player_position(self, pos: tuple):
        self.player_position = pos

    def draw(self):
        while True:
            with canvas(self.device) as draw:
                # Clear screen
                draw.rectangle(self.device.bounding_box, fill="black")

                # Draw player position
                draw.point(self.player_position, fill="white")

        sleep(500)

