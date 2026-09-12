import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)

tiempos = [1, 0.5, 2, 0.3]
# cada posicion de esta lista es el tiempo (en segundos) que espera
# ese led antes de pasar al siguiente

while True:

    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
    time.sleep(tiempos[0])
    # prende led1, espera el tiempo asignado a esa posicion (1 segundo)

    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(25, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
    time.sleep(tiempos[1])
    # prende led2, espera 0.5 segundos

    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.HIGH)
    GPIO.output(8, GPIO.LOW)
    time.sleep(tiempos[2])
    # prende led3, espera 2 segundos

    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)
    GPIO.output(8, GPIO.HIGH)
    time.sleep(tiempos[3])
    # prende led4, espera 0.3 segundos