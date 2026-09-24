import RPi.GPIO as GPIO
import serial
import time

TRIG = 23
ECHO = 24

# ---------------- UART ----------------
puerto = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# ---------------- GPIO ----------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, GPIO.LOW)

time.sleep(2)

try:
    while True:

        # Pulso de 10 microsegundos
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)

        # Esperar inicio de ECHO
        while GPIO.input(ECHO) == 0:
            inicio = time.time()

        # Esperar final de ECHO
        while GPIO.input(ECHO) == 1:
            fin = time.time()

        tiempo = fin - inicio

        distancia = (tiempo * 34300) / 2

        print("Distancia:", round(distancia, 2), "cm")

        # Enviar distancia a la TIVA
        mensaje = str(int(distancia * 10)) + "\n"
        puerto.write(mensaje.encode())

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Programa terminado")

finally:
    puerto.close()
    GPIO.cleanup()