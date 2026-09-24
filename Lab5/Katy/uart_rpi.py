import serial
import time

puerto = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

time.sleep(2)

print("UART conectado correctamente")

while True:
    dato = input("Escribe un dato para enviar a la TIVA: ")

    puerto.write(dato.encode())

    print("Dato enviado:", dato)