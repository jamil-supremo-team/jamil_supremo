cantidad = input("¿Cuántos números desea sumar?: ")
cantidad = int(cantidad)

suma_total = 0

for i in range(cantidad):

    numero = input("Ingrese un número: ")
    numero = int(numero)

    suma_total = suma_total + numero

print("La suma total es:", suma_total)