n = int(input("Cuantos numeros quiere sumar: "))

suma = 0

for i in range(n):
    numero = int(input("Ingrese un numero: "))
    suma = suma + numero

print("La suma es:", suma)