import RPi.GPIO as GPIO
import time
import random #esta libreria es nueva sirve para crear un numero al hazar del 0 al 35

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)  # LED rojo = calefactor
GPIO.setup(24, GPIO.OUT)  # Ventilador

while True:

    temperatura = random.randint(0, 35)#lo que hace es qeu genera numeros aleatorios de 0a 35
    

    print("Temperatura:", temperatura)

    if temperatura < 12:
        GPIO.output(23, GPIO.HIGH)#enciende calefactor
        GPIO.output(24, GPIO.LOW)#apaga ventilador

    elif temperatura > 20:
        GPIO.output(23, GPIO.LOW)#apaga calefactor
        GPIO.output(24, GPIO.HIGH)#enciende ventilador

    else:
        GPIO.output(23, GPIO.LOW)#apaga calefactor
        GPIO.output(24, GPIO.LOW)#apaga ventilador

    time.sleep(2)#espera 2 segundos antes de generar una nueva temperatura