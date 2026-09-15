cantidad = int(input("Cuantos numeros ingresara: "))

numeros = []

for i in range(cantidad):
    numero = int(input("Ingrese un numero: "))

    if numero not in numeros:
        numeros.append(numero)

print("Numeros sin repetir:", numeros)