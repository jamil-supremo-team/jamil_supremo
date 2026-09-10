import RPi.GPIO as GPIO
import time
import random


# -----------------------------
# PINES
# -----------------------------

leds = [17, 27, 22, 23]

but1 = 24
but2 = 25


# -----------------------------
# CONFIGURACIÓN
# -----------------------------

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


for led in leds:
    GPIO.setup(led, GPIO.OUT)


GPIO.setup(but1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but2, GPIO.IN, pull_up_down=GPIO.PUD_UP)



# -----------------------------
# VARIABLES
# -----------------------------

led_actual = None
tiempo = 1



# -----------------------------
# FUNCIONES
# -----------------------------


def apagar_leds():

    for led in leds:
        GPIO.output(led, GPIO.LOW)



def seleccionar_led():

    global led_actual
    global tiempo

    led_actual = random.choice(leds)

    tiempo = 1

    print("LED seleccionado:", led_actual)
    print("Tiempo reiniciado:", tiempo)



def aumentar_tiempo():

    global tiempo

    tiempo += 1

    print("Tiempo:", tiempo)



def encender_led():

    if led_actual != None:

        apagar_leds()

        GPIO.output(led_actual, GPIO.HIGH)

        print("LED encendido")

        time.sleep(tiempo)

        GPIO.output(led_actual, GPIO.LOW)



# -----------------------------
# PROGRAMA PRINCIPAL
# -----------------------------


while True:


    # Botón 1 selecciona LED aleatorio

    if GPIO.input(but1) == GPIO.LOW:

        seleccionar_led()

        encender_led()

        time.sleep(0.3)



    # Botón 2 aumenta tiempo

    if GPIO.input(but2) == GPIO.LOW:

        aumentar_tiempo()

        encender_led()

        time.sleep(0.3)