import cv2 as cv

class Filtros:
    def rgb(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
    def hsv(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2HSV)
        
    def gris(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


img = cv.imread("1.jpg")

filtro = Filtros()

cv.imshow("RGB", filtro.rgb(img))
cv.imshow("HSV", filtro.hsv(img))
cv.imshow("Grises", filtro.gris(img))

cv.waitKey(0)
cv.destroyAllWindows()