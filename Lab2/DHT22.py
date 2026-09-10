import time
import board
import adafruit_dht

dht = adafruit_dht.DHT22(board.D5, use_pulseio=False)

while True:

    try:
        temperatura = dht.temperature
        humedad = dht.humidity

        print("Temperatura:", temperatura, "°C")
        print("Humedad:", humedad, "%")
        print("----------------------")

    except RuntimeError:
        print("Error al leer el DHT22")

    time.sleep(2)