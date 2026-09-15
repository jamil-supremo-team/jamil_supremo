import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

while True:

    archivo = open("tiempos.txt", "r")#lo que hace esto es que lo pone el texto en modo lectura 
    tiempo1 = float(archivo.readline())#y extrae todos los valores que an sido asignados en columana
    tiempo2 = float(archivo.readline())#pero obviamente el txt tiene que estar si o si en el mismo 
    tiempo3 = float(archivo.readline())#repositorio o bueno carpeta 
    archivo.close()#y lo cierra el archivo 
    # abre el archivo, lee 3 lineas, cada una se convierte a numero, y cierra el archivo

    GPIO.output(16, GPIO.HIGH)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    time.sleep(tiempo1)

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)
    time.sleep(tiempo2)

    GPIO.output(16, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.HIGH)
    time.sleep(tiempo3)