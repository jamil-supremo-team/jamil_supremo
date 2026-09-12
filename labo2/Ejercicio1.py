import RPi.GPIO as GPIO
import time #maneja el tiempo en segundos 

#configuraciones de puertos de la placa GPIO y modo entrada o modo salida
#GPIO.setwarnings(False)#obcional para que salten alarmas 
GPIO.setmode(GPIO.BCM)#modo de conexion BCM numeracion de 1 al 40 

GPIO.setup(23, GPIO.OUT)#modo de conexiones de modo entrada 
GPIO.setup(24, GPIO.OUT)#ademas de declaracion de que pines en modo BCM
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)#modo de conexion por el boton en modo pull up por el comando 
#PUD.UP y si queira en down es PUD.DOWN


estado_actual = 1#nos dice que estado inicial entraremos para los 4 casos entonces entraremos en estado 1el inicial

UltimoCambio = time.time()#guarda el ultimo moemtno del estado del led 
EstadoLed = False # para saber que estado necesita cambiarce o para hacer el encendido variaremos en estado true 
#y false para poder cambiar 



#------------------------------------------------------------------ejecucion de bucle

while True:

    if GPIO.input(18) == GPIO.LOW:# pin 18 si detectas una pulsacion se activa porque ahora como es pull up estamos en 
        #estado 1 constantemente y si detecta es 0 entonces por eso LOW
        estado_actual += 1 #es lo mismo que decir estado_actual = estado_actual + 1
        if estado_actual > 4:#lo que hace practicamente esta cosa es si sobrepasa a un quinto estado se recetea y vuelve
            #al 1 asi trabaja 
            estado_actual = 1
        print("Estado:", estado_actual)
        time.sleep(0.3)#hal dilay 

    TiempoActual = time.time()#esta cosa guarda el tiempo actual de cada vuelta y lo almacena 

    if estado_actual == 1:#primer estado 
        if TiempoActual - UltimoCambio >= 1:

            if EstadoLed == True:#lo que hace esto es comparar constantemente lo que dice es que entra como falso 
                #lo compara y me dice si esto no sirve  paso al else que con el = lo convierte en verdad y luego vuelve 
                #al if y lo convierte en falso otra vez y asi sucesivamente una y otra vez alternando 
                EstadoLed = False
            else:
                EstadoLed = True

            if EstadoLed == True:
                GPIO.output(23, GPIO.HIGH)
                GPIO.output(24, GPIO.LOW)
            else:
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.HIGH)

            UltimoCambio = TiempoActual

    elif estado_actual == 2:#estado 2 
        if TiempoActual - UltimoCambio >= 2:#lo mismo ahora aqui pregunta que si ya paso 2 segundos 

            if EstadoLed == True:#hace el mismo bucle como arriba 
                EstadoLed = False
            else:
                EstadoLed = True

            if EstadoLed == True:
                GPIO.output(23, GPIO.HIGH)
                GPIO.output(24, GPIO.HIGH)
            else:
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.LOW)

            UltimoCambio = TiempoActual

    elif estado_actual == 3:#ahora ya no pide intervalos apra contar entocnes los enciende indefinidamente una vez 
        #que entra a este estado por eso no tiene tiempo 
        GPIO.output(23, GPIO.HIGH)
        GPIO.output(24, GPIO.HIGH)

    elif estado_actual == 4: #lo mismo queel estado 3 pero ahora los apaga
        GPIO.output(23, GPIO.LOW)
        GPIO.output(24, GPIO.LOW)