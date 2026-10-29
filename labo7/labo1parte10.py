"""
#Investiga cómo capturar la imagen de un fotograma y guardarla como una imagen usando OpenCV.
Luego, captura la imagen de la cámara web y guarda el fotograma cada vez que se presione la tecla "c"
con el formato "Captures/image1.jpg". Cuando el proceso termine, aplica un filtro de escala de grises a
la imagen y divídela en cuadrantes.
"""

import cv2

cap = cv2.VideoCapture(2)
imagen_guardada = False

while True:
    ret, frame = cap.read()
    cv2.imshow('Camara', frame)
    
    tecla = cv2.waitKey(1)
    
    if tecla == ord('c'):
        # Guarda siempre como image1.jpg (sobrescribe si ya existe)
        cv2.imwrite("Captures/image1.jpg", frame)
        imagen_guardada = True
        print("Guardado en Captures/image1.jpg")
        
    if tecla == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Aplicar filtro y dividir solo si presionaste 'c'
if imagen_guardada:
    gris = cv2.imread("Captures/image1.jpg", cv2.IMREAD_GRAYSCALE)
    
    alto, ancho = gris.shape
    y, x = alto // 2, ancho // 2
    
    # Mostrar los 4 cuadrantes
    cv2.imshow('Arriba Izquierda', gris[0:y, 0:x])
    cv2.imshow('Arriba Derecha', gris[0:y, x:ancho])
    cv2.imshow('Abajo Izquierda', gris[y:alto, 0:x])
    cv2.imshow('Abajo Derecha', gris[y:alto, x:ancho])
    
    cv2.waitKey(0)