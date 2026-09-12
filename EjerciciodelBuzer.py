import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)  # Buzzer
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Boton

while True:

    if GPIO.input(18) == GPIO.LOW:
        GPIO.output(23, GPIO.HIGH)  # enciende el buzzer
        print("Buzzer sonando")
    else:
        GPIO.output(23, GPIO.LOW)   # apaga el buzzer