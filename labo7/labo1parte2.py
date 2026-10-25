import cv2 as cv 
import numpy as np

img = cv.imread("1.jpg")

opcion = input("Elige una opción (1-4): ")

if opcion == '2':
    img = cv.resize(img, (250, 250))
elif opcion == '3':
    img = cv.resize(img, (500, 500))
elif opcion == '4':
    img = cv.resize(img, (1000, 1000))
else: # opcion == 1 
    img = img 

# Se muestra la imagen una sola vez al final
cv.imshow("final", img)

# Mantiene la ventana abierta hasta que presiones cualquier tecla
cv.waitKey(0)
cv.destroyAllWindows()