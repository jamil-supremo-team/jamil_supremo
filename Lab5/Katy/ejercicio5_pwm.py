import RPi.GPIO as GPIO
import time

IN1 = 17
IN2 = 27
ENA = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Dirección del motor
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

# Crear PWM
motor = GPIO.PWM(ENA, 1000)
motor.start(0)

try:
    motor.ChangeDutyCycle(75)
    print("Motor al 75%")
    time.sleep(5)

    motor.ChangeDutyCycle(25)
    print("Motor al 25%")
    time.sleep(5)

    motor.ChangeDutyCycle(45)
    print("Motor al 45%")
    time.sleep(5)

    motor.ChangeDutyCycle(50)
    print("Motor al 50%")
    time.sleep(5)

finally:
    motor.stop()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()