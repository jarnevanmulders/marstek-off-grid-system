import RPi.GPIO as GPIO
import time

# BCM pinnummering gebruiken
GPIO.setmode(GPIO.BCM)

PIN1 = 24
PIN2 = 25

GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)

try:
    while True:
        # Alles laag
        GPIO.output(PIN1, GPIO.LOW)
        GPIO.output(PIN2, GPIO.LOW)

        # Pin 1 hoog
        GPIO.output(PIN1, GPIO.HIGH)
        time.sleep(1)

        GPIO.output(PIN1, GPIO.LOW)

        # Pin 2 hoog
        GPIO.output(PIN2, GPIO.HIGH)
        time.sleep(1)

        GPIO.output(PIN2, GPIO.LOW)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()