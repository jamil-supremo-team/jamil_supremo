import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)  #lED bit 0
GPIO.setup(24, GPIO.OUT)  #lED bit 1
GPIO.setup(25, GPIO.OUT)  #lED bit 2
GPIO.setup(8, GPIO.OUT)   #lED bit 3

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # boton de subida y bajada
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

contador = 0

while True:

    if GPIO.input(18) == GPIO.LOW: #lo que hace esto es cambiar de fase a fase 
        contador += 1 #contador = contador + 1 
        if contador > 15:
            contador = 0
        print("Contador:", contador)
        time.sleep(0.3)

    if GPIO.input(17) == GPIO.LOW:#y lo mismo pero para contar hacia abajo 
        if contador > 0:
            contador -= 1#los mismo pero ahora cuenta para abajo para que baje 
        print("Contador:", contador)
        time.sleep(0.3)

    bit0 = contador % 2 #lo que hace esto es contar y modificar el valor actual para darle un valor actual del
    #bit y dar sentido encender o no encender y dependiendo de eso saca el valor mas significativo 0 o 1 y eso 
    #va para la salidas de los GPIO donde se hacen estas ecuaciones y en base a ese numero se enciende o se apaga 
    #0 apagado 1 encendido y asi sale como interprete los leds 
    bit1 = (contador // 2) % 2
    bit2 = (contador // 4) % 2
    bit3 = (contador // 8) % 2

    GPIO.output(23, bit0)#aqui se denota las salidas 0 apagado 1 encendido
    GPIO.output(24, bit1)
    GPIO.output(25, bit2)
    GPIO.output(8, bit3)