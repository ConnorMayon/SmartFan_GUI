import RPi.GPIO as GPIO
import time

def main():
    pin = 4

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)

    status = "off"

    while True:
        status = input()
        if status == "on":
            GPIO.output(pin, GPIO.HIGH)
        #time.sleep(6)
        if status == "off":
            GPIO.output(pin, GPIO.LOW)
        #time.sleep(6)

if __name__ == "__main__":
    main()