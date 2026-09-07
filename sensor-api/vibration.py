import RPi.GPIO as GPIO
import time

relay_pin = 13

class Vibration():
    def do(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(relay_pin, GPIO.OUT)

        for i in range(1, 10):
            GPIO.output(relay_pin, GPIO.LOW)
            time.sleep(1)
            GPIO.output(relay_pin, GPIO.HIGH)
            time.sleep(1)

        GPIO.cleanup()
