import serial
import RPi.GPIO as GPIO

IN1 = 17
IN2 = 27
ENA = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Dirección del motor
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

# PWM del motor
motor = GPIO.PWM(ENA, 1000)
motor.start(0)

# UART con la TIVA
puerto = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

while True:

    dato = puerto.read(1)

    if dato:
        porcentaje = dato[0]

        motor.ChangeDutyCycle(porcentaje)

        print("Motor:", porcentaje, "%")