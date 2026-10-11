from typing import Callable
import RPi.GPIO as GPIO
import time
import threading

class Controls:

    def __init__(self):
        self.callback_up: Callable[[bool], None] | None = None
        self.callback_down: Callable[[bool], None] | None = None
        self.callback_left: Callable[[bool], None] | None = None
        self.callback_right: Callable[[bool], None] | None = None

        self.button_up = 37
        self.button_down = 33
        self.button_left = 22
        self.button_right = 35

        # GPIO setup
        GPIO.setmode(GPIO.BOARD)

        # Setup all buttons
        GPIO.setup(self.button_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button_left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.button_right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Callbacks
    def _internal_callback_up(self, channel: int):
        is_pressed = GPIO.input(channel) == GPIO.LOW
        if self.callback_up:
            self.callback_up(is_pressed)

    def _internal_callback_down(self, channel: int):
        is_pressed = GPIO.input(channel) == GPIO.LOW
        if self.callback_down:
            self.callback_down(is_pressed)

    def _internal_callback_left(self, channel: int):
        is_pressed = GPIO.input(channel) == GPIO.LOW
        if self.callback_left:
            self.callback_left(is_pressed)

    def _internal_callback_right(self, channel: int):
        is_pressed = GPIO.input(channel) == GPIO.LOW
        if self.callback_right:
            self.callback_right(is_pressed)

    def start(
        self,
        callback_up: Callable[[bool], None],
        callback_down: Callable[[bool], None],
        callback_left: Callable[[bool], None],
        callback_right: Callable[[bool], None]
    ):
        self.callback_up = callback_up
        self.callback_down = callback_down
        self.callback_left = callback_left
        self.callback_right = callback_right

        print("testificate")

        # Add callbacks
        GPIO.add_event_detect(
            self.button_up, GPIO.RISING, callback=self._internal_callback_up, bouncetime=200
        )
        GPIO.add_event_detect(
            self.button_down, GPIO.RISING, callback=self._internal_callback_down, bouncetime=200
        )
        GPIO.add_event_detect(
            self.button_left, GPIO.RISING, callback=self._internal_callback_left, bouncetime=200
        )
        GPIO.add_event_detect(
            self.button_right, GPIO.RISING, callback=self._internal_callback_right, bouncetime=200
        )
