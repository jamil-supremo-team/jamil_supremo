import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)  # Buzzer

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Boton encender
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Boton apagar

buzzer_encendido = False

while True:

    if GPIO.input(18) == GPIO.LOW:
        buzzer_encendido = True
        print("Buzzer encendido")
        time.sleep(0.3)

    if GPIO.input(17) == GPIO.LOW:
        buzzer_encendido = False
        print("Buzzer apagado")
        time.sleep(0.3)

    if buzzer_encendido == True:
        GPIO.output(23, GPIO.HIGH)
    else:
        GPIO.output(23, GPIO.LOW)