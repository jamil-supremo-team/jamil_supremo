import RPi.GPIO as GPIO
import time

led1 = 23
led2 = 24
but = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(but, GPIO.IN, pull_up_down=GPIO.PUD_UP)

std = 1

UltimoCambio = time.time()
EstadoLed = False


def estado1(TiempoActual):
    global UltimoCambio
    global EstadoLed

    if TiempoActual - UltimoCambio >= 1:

        EstadoLed = not EstadoLed

        GPIO.output(led1, EstadoLed)
        GPIO.output(led2, not EstadoLed)

        UltimoCambio = TiempoActual


def estado2(TiempoActual):
    global UltimoCambio
    global EstadoLed

    if TiempoActual - UltimoCambio >= 2:

        EstadoLed = not EstadoLed

        GPIO.output(led1, EstadoLed)
        GPIO.output(led2, EstadoLed)

        UltimoCambio = TiempoActual


def estado3():
    GPIO.output(led1, GPIO.HIGH)
    GPIO.output(led2, GPIO.HIGH)


def estado4():
    GPIO.output(led1, GPIO.LOW)
    GPIO.output(led2, GPIO.LOW)


while True:

    if GPIO.input(but) == GPIO.LOW:
        std += 1

        if std > 4:
            std = 1

        print("Estado:", std)
        time.sleep(0.2)

    TiempoActual = time.time()

    if std == 1:
        estado1(TiempoActual)

    elif std == 2:
        estado2(TiempoActual)

    elif std == 3:
        estado3()

    elif std == 4:
        estado4()