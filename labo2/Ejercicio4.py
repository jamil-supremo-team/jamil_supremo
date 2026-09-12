import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led_actual = 0        #indica cual led esta seleccionado (0, 1, 2 o 3)
tiempo_encendido = 1  #segundos que el led debe permanecer encendido
tiempo_inicio = time.time()  #momento en que se encendio el led actual

while True:

    if GPIO.input(18) == GPIO.LOW:#sistema de los botones como en el 1 uno sube otro baja
        led_actual += 1#led actual = led actual + 1
        if led_actual > 3: #esto sirve para reinciar el contador 
            led_actual = 0
        tiempo_encendido = 1
        tiempo_inicio = time.time()
        print("Led seleccionado:", led_actual, "Tiempo:", tiempo_encendido)
        time.sleep(0.3)

    if GPIO.input(17) == GPIO.LOW:#esto hace que por cada presion del boton se guarde el segundo extra o un nuevo tiempo 
        tiempo_encendido += 1#por esto el tiempo se actualiza de 1 a 2 luego 3 cada pulsacion 
        print("Nuevo tiempo:", tiempo_encendido)
        time.sleep(0.3)

    tiempo_actual = time.time()# guarda el tiempo que se esta contando

    GPIO.output(23, GPIO.LOW) #los ponemos en apagados todos los leds para empezar  en inicio
    GPIO.output(24, GPIO.LOW)
    GPIO.output(25, GPIO.LOW)
    GPIO.output(8, GPIO.LOW)
   

    if tiempo_actual - tiempo_inicio < tiempo_encendido:
        #si todavia no se cumple el tiempo, prende el led seleccionado

        if led_actual == 0:
            GPIO.output(23, GPIO.HIGH) #encendido y apagado de los leds uno por 1 dependiendo del tiempo o del estado del que esten en secuencia
        elif led_actual == 1:
            GPIO.output(24, GPIO.HIGH)
        elif led_actual == 2:
            GPIO.output(25, GPIO.HIGH)
        elif led_actual == 3:
            GPIO.output(8, GPIO.HIGH)