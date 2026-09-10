import RPi.GPIO as GPIO
import time

led1 = 23
led2 = 24
but = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(but, GPIO.IN, pull_up_down=GPIO.PUD_UP)

std = 1


while True:

    if GPIO.input(but) == GPIO.LOW:
        std += 1
        if std > 4:
            std = 1
        print("Estado:", std)
        time.sleep(0.5)


    if std == 1:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.HIGH)
        time.sleep(1)


    elif std == 2:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        time.sleep(2)


    elif std == 3:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)


    elif std == 4:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)