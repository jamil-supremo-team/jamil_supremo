import cv2 as cv

# Primera imagen
img1 = cv.imread("rojo.jpg")
img1_rgb = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
print("rojo.jpg:", img1_rgb[0, 0])

# Segunda imagen
img2 = cv.imread("verde.jpg")
img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
print("verde.jpg:", img2_rgb[0, 0])

# Tercera imagen
img3 = cv.imread("azul.jpg")
img3_rgb = cv.cvtColor(img3, cv.COLOR_BGR2RGB)
print("azul.jpg:", img3_rgb[0, 0])
