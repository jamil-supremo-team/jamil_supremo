import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def boton_cambiar_presionado():#aumento para presion de boton2 
    return GPIO.input(18) == GPIO.LOW


def boton_aumentar_presionado():#aumento para presion de boton 1 
    return GPIO.input(17) == GPIO.LOW


def siguiente_led(led):#reinicio de leds
    nuevo = led + 1
    if nuevo > 3:
        nuevo = 0
    return nuevo


def apagar_todos():
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)


def prender_led(led):#estados encendiod de leds
    if led == 0:
        GPIO.output(23, GPIO.HIGH)
    elif led == 1:
        GPIO.output(24, GPIO.HIGH)
    elif led == 2:
        GPIO.output(25, GPIO.HIGH)
    elif led == 3:
        GPIO.output(8, GPIO.HIGH)


led_actual = 0
tiempo_encendido = 1
tiempo_inicio = time.time()

while True:

    if boton_cambiar_presionado():
        led_actual = siguiente_led(led_actual)
        tiempo_encendido = 1
        tiempo_inicio = time.time()
        print("Led seleccionado:", led_actual, "Tiempo:", tiempo_encendido)
        time.sleep(0.3)

    if boton_aumentar_presionado():
        tiempo_encendido += 1
        print("Nuevo tiempo:", tiempo_encendido)
        time.sleep(0.3)

    tiempo_actual = time.time()

    apagar_todos()

    if tiempo_actual - tiempo_inicio < tiempo_encendido:
        prender_led(led_actual)