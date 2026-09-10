import RPi.GPIO as GPIO
import time
import board
import adafruit_dht

# Pines
led_calefactor = 23
ventilador = 24

# DHT22 en GPIO5
dht = adafruit_dht.DHT22(board.D5, use_pulseio=False)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(led_calefactor, GPIO.OUT)
GPIO.setup(ventilador, GPIO.OUT)

while True:

    try:

        temperatura = dht.temperature
        humedad = dht.humidity

        print("Temperatura:", temperatura, "°C")
        print("Humedad:", humedad, "%")

        # Si la temperatura es menor a 12°C
        if temperatura < 27:

            GPIO.output(led_calefactor, GPIO.HIGH)
            GPIO.output(ventilador, GPIO.LOW)

            print("Calefactor ENCENDIDO")
            print("Ventilador APAGADO")


        # Si la temperatura es mayor a 20°C
        elif temperatura > 40:

            GPIO.output(led_calefactor, GPIO.LOW)
            GPIO.output(ventilador, GPIO.HIGH)

            print("Calefactor APAGADO")
            print("Ventilador ENCENDIDO")


        # Si está entre 12°C y 20°C
        else:

            GPIO.output(led_calefactor, GPIO.LOW)
            GPIO.output(ventilador, GPIO.LOW)

            print("Temperatura OPTIMA")
            print("Calefactor APAGADO")
            print("Ventilador APAGADO")

        print("-------------------------")

    except RuntimeError:

        print("Error al leer el DHT22")

    time.sleep(2)