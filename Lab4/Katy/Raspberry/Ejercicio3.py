import RPi.GPIO as GPIO
import time

#----------------PINES DE LED-------------#
LED1 = 23
LED2 = 24
LED3 = 25
LED4 = 8

#----------------CONFIGURACION------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)

GPIO.output(LED1, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)
GPIO.output(LED3, GPIO.LOW)
GPIO.output(LED4, GPIO.LOW)

#----------------VARIABLE-----------------#
estado = 1

#----------------LOGICA-------------------#
while True:

    archivo = open("tiempo.txt", "r")
    intervalo = float(archivo.read())
    archivo.close()

    GPIO.output(LED1, GPIO.LOW)
    GPIO.output(LED2, GPIO.LOW)
    GPIO.output(LED3, GPIO.LOW)
    GPIO.output(LED4, GPIO.LOW)

    if estado == 1:
        GPIO.output(LED1, GPIO.HIGH)

    elif estado == 2:
        GPIO.output(LED2, GPIO.HIGH)

    elif estado == 3:
        GPIO.output(LED3, GPIO.HIGH)

    elif estado == 4:
        GPIO.output(LED4, GPIO.HIGH)

    
    time.sleep(intervalo)


    estado = estado + 1

    if estado > 4:
        estado = 1