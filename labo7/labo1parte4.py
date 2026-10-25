import cv2 as cv

img = cv.imread("1.jpg")
cv.imshow("Original", img)

img_resized = cv.resize(img, (400, 600))

mitad_superior = img_resized[:300, :]
mitad_inferior = img_resized[300:, :]
cv.imshow("Mitad Superior", mitad_superior)
cv.imshow("Mitad Inferior", mitad_inferior)

mitad_izquierda = img_resized[:, :200]
mitad_derecha = img_resized[:, 200:]
cv.imshow("Mitad Izquierda", mitad_izquierda)
cv.imshow("Mitad Derecha", mitad_derecha)

cuadrante_1 = img_resized[:300, :200]
cuadrante_2 = img_resized[:300, 200:]
cuadrante_3 = img_resized[300:, :200]
cuadrante_4 = img_resized[300:, 200:]

cv.imshow("Cuadrante 1", cuadrante_1)
cv.imshow("Cuadrante 2", cuadrante_2)
cv.imshow("Cuadrante 3", cuadrante_3)
cv.imshow("Cuadrante 4", cuadrante_4)

cv.waitKey(0)
cv.destroyAllWindows()