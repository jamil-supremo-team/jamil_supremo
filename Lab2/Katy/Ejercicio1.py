import RPi.GPIO as GPIO
import time

 #----------------PINES DE LED------------#
LED1 = 23 
LED2 = 24

#------------------PINE DEL BOTON---------#
BOTON = 22
estado = 1

#-----------CONFIGURACION DE PINES--------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED1,GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(BOTON, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.output(LED1, GPIO.LOW)
GPIO.output(LED2, GPIO.LOW)

#----------------LOGICA---------------------#
while True:
    
    bot_actual = GPIO.input(BOTON)

    if bot_actual:
        estado = estado + 1

        if estado > 4:
            estado = 1

        time.sleep(0.05)

    if estado == 1:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.LOW)
        time.sleep(1)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.HIGH)
        time.sleep(1)

    elif estado == 2:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)
        time.sleep(2)

    elif estado == 3:
        GPIO.output(LED1, GPIO.HIGH)
        GPIO.output(LED2, GPIO.HIGH)

    elif estado == 4:
        GPIO.output(LED1, GPIO.LOW)
        GPIO.output(LED2, GPIO.LOW)