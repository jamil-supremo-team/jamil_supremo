import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#estas son funciones se crea con def y return y se declaran dandole un nombre y luego que valor es el que hacen 
# #funcionar  
def siguiente_estado(estado): #definimos el conteo de estados para pasar de estado a estado 
    nuevo = estado + 1
    if nuevo > 4:
        nuevo = 1
    return nuevo


def invertir(valor):#este es el bucle 
    if valor == True:
        return False
    else:
        return True


def salida_estado_1(led_encendido):#accion de cada estado 1
    if led_encendido == True:
        return (GPIO.HIGH, GPIO.LOW)
    else:
        return (GPIO.LOW, GPIO.HIGH)


def salida_estado_2(led_encendido):#estado 2 
    if led_encendido == True:
        return (GPIO.HIGH, GPIO.HIGH)
    else:
        return (GPIO.LOW, GPIO.LOW)


def salida_estado_3():#estado 3
    return (GPIO.HIGH, GPIO.HIGH)


def salida_estado_4():#estado 4
    return (GPIO.LOW, GPIO.LOW)


def boton_presionado():#accion del boton en pull up 
    return GPIO.input(18) == GPIO.LOW


# --- variablesiniciales ---
estado_actual = 1
ultimo_cambio = time.time()
led_encendido = False




#------inicio de bucle
while True: #bucle

    if boton_presionado():#para iniciar el boton llama al boton presionado o el def de arriba y cambia de estado 
        estado_actual = siguiente_estado(estado_actual)
        print("Estado:", estado_actual)
        time.sleep(0.3)

    tiempo_actual = time.time()

    if estado_actual == 1:#estado 1 
        if tiempo_actual - ultimo_cambio >= 1:
            led_encendido = invertir(led_encendido)
            valor1, valor2 = salida_estado_1(led_encendido)
            GPIO.output(23, valor1)
            GPIO.output(24, valor2)
            ultimo_cambio = tiempo_actual

    elif estado_actual == 2:#estado 2
        if tiempo_actual - ultimo_cambio >= 2:
            led_encendido = invertir(led_encendido)
            valor1, valor2 = salida_estado_2(led_encendido)
            GPIO.output(23, valor1)
            GPIO.output(24, valor2)
            ultimo_cambio = tiempo_actual

    elif estado_actual == 3:#estado 3
        valor1, valor2 = salida_estado_3()
        GPIO.output(23, valor1)
        GPIO.output(24, valor2)

    elif estado_actual == 4:#estado 4
        valor1, valor2 = salida_estado_4()
        GPIO.output(23, valor1)
        GPIO.output(24, valor2)