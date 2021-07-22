import RPi.GPIO as GPIO
from datetime import datetime
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led_bar_G = 23 # Green
led_bar_R = 18 # Red
led_bar_Y = 12 # Yellow

GPIO.setup(led_bar_G, GPIO.OUT)
GPIO.setup(led_bar_R, GPIO.OUT)
GPIO.setup(led_bar_Y, GPIO.OUT)

GPIO.output(led_bar_G, GPIO.HIGH)
GPIO.output(led_bar_R, GPIO.HIGH)

while True:
    now = datetime.now()
    print(now.hour, "H", now.minute, "minute", now.second,"second")
    if (now.hour == 23 or now.hour == 24 or ( now.hour > 0 and now.hour < 5 )):
        GPIO.output(led_bar_Y, GPIO.HIGH)
    else:
        GPIO.output(led_bar_Y, GPIO.LOW)

    time.sleep(1)
