import serial
import time

puerto = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

time.sleep(2)

while True:
    segundos = input("Ingrese segundos (1-9): ")

    puerto.write(segundos.encode())

    print("Timer cambiado a", segundos, "segundos")