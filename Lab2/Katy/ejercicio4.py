import RPi.GPIO as GPIO
import time

#--------------PINES DEL LED--------------#
LED1 = 23
LED2 = 24
LED3 = 25
LED4 = 8

#--------------PINES DEL BOTON------------#
BOTON1 = 22
BOTON2 = 27

#---------------VARIABLES------------------#
led_sel = 1
tiempo = 1

#---------------CONFIGURACION--------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LED3, GPIO.OUT)
GPIO.setup(LED4, GPIO.OUT)
GPIO.setup(BOTON1, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BOTON2, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.output(LED1, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)
GPIO.output(LED3, GPIO.LOW)
GPIO.output(LED4, GPIO.LOW)

#----------------------LOGICA-------------------#
while True:
    bot1_actual = GPIO.input(BOTON1)
    bot2_actual = GPIO.input(BOTON2)

    activar = False

    if bot1_actual:
        led_sel = led_sel + 1
        if led_sel > 4:
            led_sel = 1
        tiempo = 1

        while GPIO.input(BOTON1) == 1:
            time.sleep(0.05)
        activar = True

    if bot2_actual:
        tiempo =  tiempo + 1

        while GPIO.input(BOTON2) == 1:
            time.sleep(0.05)

        activar = True

    if activar:
        if led_sel == 1:
            GPIO.output(LED1, GPIO.HIGH)

        elif led_sel == 2:
            GPIO.output(LED2, GPIO.HIGH)

        elif led_sel == 3:
            GPIO.output(LED3, GPIO.HIGH)

        elif led_sel == 4:
            GPIO.output(LED4, GPIO.HIGH)

        time.sleep(tiempo)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        GPIO.output(LED3, GPIO.LOW)
        GPIO.output(LED4, GPIO.LOW)