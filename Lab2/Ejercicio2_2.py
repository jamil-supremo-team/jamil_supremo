import RPi.GPIO as GPIO
import time

led1 = 17
led2 = 27
led3 = 22
led4 = 23

but1 = 24
but2 = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.setup(led4, GPIO.OUT)

GPIO.setup(but1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(but2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

contador = 0


def mostrar_valor():
    print("Decimal:", contador)
    print("Binario:", bin(contador))
    print("Hexadecimal:", hex(contador))


def incrementar():
    global contador

    contador += 1

    if contador > 15:
        contador = 0

    mostrar_valor()


def decrementar():
    global contador

    contador -= 1

    if contador < 0:
        contador = 0

    mostrar_valor()


def actualizar_leds():

    if contador == 0:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 1:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 2:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 3:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 4:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 5:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 6:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 7:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.LOW)

    elif contador == 8:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 9:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 10:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 11:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.LOW)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 12:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 13:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.LOW)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 14:
        GPIO.output(led1, GPIO.LOW)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.HIGH)

    elif contador == 15:
        GPIO.output(led1, GPIO.HIGH)
        GPIO.output(led2, GPIO.HIGH)
        GPIO.output(led3, GPIO.HIGH)
        GPIO.output(led4, GPIO.HIGH)


while True:

    if GPIO.input(but1) == GPIO.LOW:
        incrementar()
        time.sleep(0.3)

    if GPIO.input(but2) == GPIO.LOW:
        decrementar()
        time.sleep(0.3)

    actualizar_leds()