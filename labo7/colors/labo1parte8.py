import cv2 as cv

rojo = cv.imread("rojo.jpg")
verde = cv.imread("verde.jpg")
azul = cv.imread("azul.jpg")


rojo1 = cv.cvtColor(rojo, cv.COLOR_BGR2HSV)[0, 0]
verde2 = cv.cvtColor(verde, cv.COLOR_BGR2HSV)[0, 0]
azul3 = cv.cvtColor(azul, cv.COLOR_BGR2HSV)[0, 0]

print("Rojo HSV:", rojo1)
print("Verde HSV:", verde2)
print("Azul HSV:", azul3)
