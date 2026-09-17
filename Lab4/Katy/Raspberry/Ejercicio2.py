import RPi.GPIO as GPIO
import time

#------------PINES----------------#
BUZZER = 23
BOTON1 = 24
BOTON2 = 25

#---------CONFIGURACION------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUZZER, GPIO.OUT)

GPIO.setup(BOTON1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOTON2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.output(BUZZER, GPIO.LOW)

#------------VARIABLE--------------#
estado_buzzer = 0

#-------------LOGICA---------------#
while True:

    boton1_actual = GPIO.input(BOTON1)
    boton2_actual = GPIO.input(BOTON2)

    if boton1_actual:
        estado_buzzer = 1

    if boton2_actual:
        estado_buzzer = 0

    if estado_buzzer == 1:
        GPIO.output(BUZZER, GPIO.HIGH)

    else:
        GPIO.output(BUZZER, GPIO.LOW)

    time.sleep(0.05)