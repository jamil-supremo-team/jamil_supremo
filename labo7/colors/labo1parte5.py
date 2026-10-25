import cv2 as cv

# Primera imagen
img1 = cv.imread("colors/rojo.jpg")
img1_rgb = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
print("rojo.jpg:", img1_rgb[0, 0])

# Segunda imagen
img2 = cv.imread("colors/verde.jpg")
img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
print("verde.jpg:", img2_rgb[0, 0])

# Tercera imagen
img3 = cv.imread("colors/azul.jpg")
img3_rgb = cv.cvtColor(img3, cv.COLOR_BGR2RGB)
print("azul.jpg:", img3_rgb[0, 0])