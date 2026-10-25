import cv2 as cv

img = cv.imread("1.jpg")

cv.imshow("Imagen 1 ", img)

nuevas_dimensiones = (1000, 1000)

redimension = cv.resize(img, nuevas_dimensiones)

cv.imshow('Imagen a 1000x1000', redimension)

cv.waitKey(0)
cv.destroyAllWindows()


