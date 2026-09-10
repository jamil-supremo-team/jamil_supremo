import RPi.GPIO as GPIO  # Librari that permit controler GPIO
import time # Librari of user for creat delay


led_pin = 12  # PIN defintions

GPIO.setwarnings(False) # Evitamso las advertecnias de los PINES GPIO
GPIO.setmode(GPIO.BCM)  # Identificamos los pins por su GPIO
                        # BCM: es para poder programar en los pines GPIO de la placa
                        # BOARD: es para programar los pines de pines de la paca por numeros

GPIO.setup(led_pin, GPIO.OUT) # Configuramos el pin como salida.

while True: # es el siclo infinito de ejecucion de el programa

    GPIO.output(led_pin, GPIO.HIGH) # Ponemos en esatdo alto
    time.sleep(1) # Delay de 1 segundo

    GPIO.output(led_pin, GPIO.LOW) # Ponemos en esatdo  bajo
    time.sleep(1) # Delay de 1 segundo