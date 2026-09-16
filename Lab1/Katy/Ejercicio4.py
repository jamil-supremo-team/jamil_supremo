cantidad = input("¿Cuántos números desea ingresar?: ")
cantidad = int(cantidad)

numeros_unicos = []

for i in range(cantidad):

    numero = input("Ingrese un número: ")
    numero = int(numero)

    if numero not in numeros_unicos:
        numeros_unicos = numeros_unicos + [numero]

print("Valores únicos:", numeros_unicos)