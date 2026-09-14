import RPi.GPIO as GPIO
import time

 #----------------PINES DE LED------------#
LED1 = 23 
LED2 = 24
LED3 = 25
LED4 = 8

#------------------PINE DEL BOTON---------#
BOTON1 = 22
BOTON2 = 27

contador = 0

#-----------CONFIGURACION DE PINES--------#
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

#-----------------LOGICA-------------------#
while True:
    bot_actual1 = GPIO.input(BOTON1)
    bot_actual2 = GPIO.input(BOTON2)

    if bot_actual1:
        contador = contador + 1
        if contador > 15:
            contador = 0

        while GPIO.input(BOTON1) == 1:
            time.sleep(0.05)
    
        print("Decimal:", contador)
        print("Binario:", f"{contador:04b}")
        print("Hexadecimal:", f"{contador:X}")


    if bot_actual2:
        if contador > 0:
            contador = contador -1

        while GPIO.input(BOTON2) == 1:
            time.sleep(0.05)
        
        print("Decimal:", contador)
        print("Binario:", f"{contador:04b}")
        print("Hexadecimal:", f"{contador:X}")

    bit1 = (contador // 8) % 2
    bit2 = (contador // 4) % 2
    bit3 = (contador // 2) % 2
    bit4 = (contador) % 2

    GPIO.output(LED1, bit1)
    GPIO.output(LED2, bit2)
    GPIO.output(LED3, bit3)
    GPIO.output(LED4, bit4)


