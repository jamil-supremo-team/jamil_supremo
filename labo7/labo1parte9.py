""""
5. Abre una cámara web usando OpenCV y muestra el fotograma en escala de grises y luego en RGB.
Cambia entre escala de grises y RGB usando las teclas del teclado.
"""
import cv2

cap = cv2.VideoCapture(2)
color = True  # Empezamos en modo color

while True:
    ret, frame = cap.read()
    
    # Mostrar la imagen según el modo elegido
    if color:
        cv2.imshow('Camara', frame)
    else:
        cv2.imshow('Camara', cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        
    # Leer el teclado
    tecla = cv2.waitKey(1)
    
    if tecla == ord('c'): color = True   # 'c' para Color
    if tecla == ord('g'): color = False  # 'g' para Gris
    if tecla == ord('q'): break          # 'q' para Salir

cap.release()
cv2.destroyAllWindows()
