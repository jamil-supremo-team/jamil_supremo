import RPi.GPIO as GPIO
import time

IN1 = 17
IN2 = 27
ENA = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

motor = GPIO.PWM(ENA, 1000)
motor.start(0)

potencia = 0

while True:

    motor.ChangeDutyCycle(potencia)

    print("PWM:", potencia, "%")

    time.sleep(0.5)

    potencia = potencia + 1

    if potencia > 100:
        potencia = 0