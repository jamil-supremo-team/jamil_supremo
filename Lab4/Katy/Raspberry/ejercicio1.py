import RPi.GPIO as GPIO
import time

#------------BUZZER----------------#
BUZZER = 23 
BOTON = 24

#-------------CONFIGURACION--------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BOTON, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.output(BUZZER, GPIO.LOW)

#-----------LOGICA-----------------#
while True:
    boton_actual = GPIO.input(BOTON)

    if boton_actual:
        GPIO.output(BUZZER, GPIO.HIGH)
    else:
        GPIO.output(BUZZER, GPIO.LOW)

    time.sleep(0.05)