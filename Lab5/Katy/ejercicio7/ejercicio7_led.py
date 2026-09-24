import serial
import RPi.GPIO as GPIO

LED = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)

pwm = GPIO.PWM(LED, 1000)
pwm.start(0)

puerto = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

while True:

    dato = puerto.read(1)

    if dato:
        porcentaje = dato[0]

        pwm.ChangeDutyCycle(porcentaje)

        print("PWM:", porcentaje, "%")