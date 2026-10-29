import cv2 as cv

# Función simple: saca el promedio de los 3 valores
def rgb_a_gris(pixel):
    r = int(pixel[0])
    g = int(pixel[1])
    b = int(pixel[2])
    return (r + g + b) // 3

# Primera imagen
img1 = cv.imread("rojo.jpg")
img1_rgb = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
print("rojo.jpg:", img1_rgb[0, 0], "-> Gris:", rgb_a_gris(img1_rgb[0, 0]))

# Segunda imagen
img2 = cv.imread("verde.jpg")
img2_rgb = cv.cvtColor(img2, cv.COLOR_BGR2RGB)
print("verde.jpg:", img2_rgb[0, 0], "-> Gris:", rgb_a_gris(img2_rgb[0, 0]))

# Tercera imagen
img3 = cv.imread("azul.jpg")
img3_rgb = cv.cvtColor(img3, cv.COLOR_BGR2RGB)
print("azul.jpg:", img3_rgb[0, 0], "-> Gris:", rgb_a_gris(img3_rgb[0, 0]))
