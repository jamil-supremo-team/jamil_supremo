import RPi.GPIO as GPIO
import time
import board #esta libreria sirve para que literalmente reconozca la placa de rasberry como algo universal 
#sin esto no seria tan facil buscar en que pines digitales pueda usar como si fuera un arduino 
import adafruit_dht #libreria especifica para hablar con el sensor dht22 y su hermano dht11

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)#lED rojo = calefactor
GPIO.setup(24, GPIO.OUT)#ventilador

sensor = adafruit_dht.DHT22(board.D4)#crea el objeto sensor, indicando que esta conectado al pin GPIO 4

while True:

    try:
        temperatura = sensor.temperature
        # le pide al sensor la temperatura actual en grados Celsius

        print("Temperatura:", temperatura)

        if temperatura < 12:
            GPIO.output(23, GPIO.HIGH)  # enciende calefactor
            GPIO.output(24, GPIO.LOW)   # apaga ventilador

        elif temperatura > 20:
            GPIO.output(23, GPIO.LOW)   # apaga calefactor
            GPIO.output(24, GPIO.HIGH)  # enciende ventilador

        else:
            GPIO.output(23, GPIO.LOW)   # apaga calefactor
            GPIO.output(24, GPIO.LOW)   # apaga ventilador

    except RuntimeError:
        print("Error leyendo el sensor, intentando de nuevo...")
        # el DHT22 a veces falla al leer, esto evita que el programa se detenga

    time.sleep(2)
    # el DHT22 necesita al menos 2 segundos entre lecturas