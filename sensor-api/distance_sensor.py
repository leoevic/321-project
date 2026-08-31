from time import sleep, time
import RPi.GPIO as GPIO
import threading
import dht11

GPIO.setmode(GPIO.BOARD)

TRIG = 36
ECHO = 32

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False);

class DistanceSensor():
    def update(self):
        while True:
            GPIO.output(TRIG, True)
            sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulse_start = time()

            while GPIO.input(ECHO)==1:
                pulse_end = time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            self.result = distance

            sleep(2)

    def __init__(self):
        self.result = 0
        threading.Thread(target=self.update, daemon=True).start()

    def readDistance(self):
        return self.result
