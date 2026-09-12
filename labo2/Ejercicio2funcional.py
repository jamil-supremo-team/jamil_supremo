import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def boton_subir_presionado():
    return GPIO.input(18) == GPIO.LOW


def boton_bajar_presionado():
    return GPIO.input(17) == GPIO.LOW


def sumar(valor):
    nuevo = valor + 1
    if nuevo > 15:
        nuevo = 0
    return nuevo


def restar(valor):
    if valor > 0:
        return valor - 1
    else:
        return valor


def obtener_bit0(valor):
    return valor % 2


def obtener_bit1(valor):
    return (valor // 2) % 2


def obtener_bit2(valor):
    return (valor // 4) % 2


def obtener_bit3(valor):
    return (valor // 8) % 2


contador = 0

while True:#lo mismo agarramos el bucle y llamamos de la misma manera como el sin funcion pero ahora solo los llamamos
    #para restar y sumar para los contador para subir o bajar con los botones y actualizamos los 
    #valores en bit 0 

    if boton_subir_presionado():
        contador = sumar(contador)
        print("Contador:", contador)
        time.sleep(0.3)

    if boton_bajar_presionado():
        contador = restar(contador)
        print("Contador:", contador)
        time.sleep(0.3)

    bit0 = obtener_bit0(contador)
    bit1 = obtener_bit1(contador)
    bit2 = obtener_bit2(contador)
    bit3 = obtener_bit3(contador)

    GPIO.output(23, bit0)
    GPIO.output(24, bit1)
    GPIO.output(25, bit2)
    GPIO.output(8, bit3)