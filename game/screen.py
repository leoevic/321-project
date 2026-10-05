import re
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class Screen:
    def __init__(self):
        self.serial = spi(port=0, device=1, gpio=noop())
        device = max7219(self.serial, cascaded=1, block_orientation=0, rotate=0)
        device.clear()
        msg = "A"

        # Draw one dot
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, fill="black")

        print("There's nothing we can do")

        while(True):
            noop()

        # show_message(self.device, msg, fill="white", font=CP437_FONT, scroll_delay=0.5)