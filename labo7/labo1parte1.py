import cv2 as cv

img = cv.imread('1.jpg')
img = cv.resize(img, (1000, 1000))
cv.imshow('facilito', img)

cv.waitKey(0)
cv.destroyAllWindows()