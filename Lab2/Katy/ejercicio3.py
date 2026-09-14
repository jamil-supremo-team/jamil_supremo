import RPI.GPIO as GPIO
import time
import random

#---------------------PINES DEL LED----------------#
CALEFACTOR = 24
VENTILADOR = 25

#----------------------CONFIGURACION---------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(CALEFACTOR,GPIO.OUT)
GPIO.setup(VENTILADOR, GPIO.OUT)

GPIO.output(CALEFACTOR, GPIO.LOW)
GPIO.output(VENTILADOR, GPIO.LOW)

#-----------------------LOGICA---------------------#
while True:
    temperatura = random.randint(0 , 30)

    if temperatura < 12:
        GPIO.output(CALEFACTOR, GPIO.HIGH)
        GPIO.output(VENTILADOR, GPIO.LOW)
        print("CALEFACTOR PRENDIDO:")

    elif temperatura > 20:
        GPIO.output(VENTILADOR, GPIO.HIGH)
        GPIO.output(CALEFACTOR, GPIO.LOW)
        print("VENTILADOR PRENDIDO")

    else:
        GPIO.output(VENTILADOR, GPIO.LOW)
        GPIO.output(CALEFACTOR, GPIO.LOW)

        print("ventilador y calefactor APAGADOS")

    print("Tempratura:", temperatura, "°C")
    time.sleep(1)

