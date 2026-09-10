import RPi.GPIO as GPIO
import time
import random

led_calefactor = 23
ventilador = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_calefactor, GPIO.OUT)
GPIO.setup(ventilador, GPIO.OUT)

while True:

    temperatura = random.randint(5, 30)

    print("Temperatura:", temperatura, "°C")

    if temperatura < 12:

        GPIO.output(led_calefactor, GPIO.HIGH)
        GPIO.output(ventilador, GPIO.LOW)

        print("Calefactor ENCENDIDO")
        print("Ventilador APAGADO")

    elif temperatura > 20:

        GPIO.output(led_calefactor, GPIO.LOW)
        GPIO.output(ventilador, GPIO.HIGH)

        print("Calefactor APAGADO")
        print("Ventilador ENCENDIDO")

    else:

        GPIO.output(led_calefactor, GPIO.LOW)
        GPIO.output(ventilador, GPIO.LOW)

        print("Temperatura OPTIMA")
        print("Calefactor APAGADO")
        print("Ventilador APAGADO")

    print("------------------------")

    time.sleep(2)