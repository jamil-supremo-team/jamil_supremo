# I(x,y) - IMAGE
# I(x,y,c) - BINARY/GRAY/COLOR IMAGE
# I(x,y,t,c) - VIDEO

# FPS: cantidad de frames por segundo
# Relación de frames con el tiempo: delay = 1/FPS

# La forma más sencilla para saber si una imagen cambió
# con respecto a otra es la resta.
# La forma más sencilla de encontrar la diferencia entre píxeles.

import cv2
import numpy as np

cap = cv2.VideoCapture("video.avi")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

step = max(1, round(2 * fps))
index = 0

# Personal
activity_vector = []

# Video resumido
codec = cv2.VideoWriter_fourcc(*"MJPG")
writer = cv2.VideoWriter(
    "summary.avi", codec, fps, (width, height))

ok, frame = cap.read()

if ok:
    print(frame.shape)
    cv2.imwrite("first_frame.jpg", frame)

    # MOG
    background = cv2.createBackgroundSubtractorMOG2(
        detectShadows=False)
    kernel = np.ones((3, 3), np.uint8)

    # Keyframes
    warmup = round(2 * fps)

    # Imagen en escala de grises
    previous = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    while True:

        # Mostrar video original
        cv2.imshow("video.avi", frame)

        # Guardar frames cada 2 segundos
        if index % step == 0:
            cv2.imwrite(
                f"frames/frame_{index:04d}.jpg", frame)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

        # Cambio de pixeles
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        difference = cv2.absdiff(gray, previous)

        _, mask_changes = cv2.threshold(
            difference, 25, 255, cv2.THRESH_BINARY)

        cv2.imshow("Changes", mask_changes)

        # MOG
        mask = background.apply(frame)

        # Opening
        mask = cv2.morphologyEx(
            mask, cv2.MORPH_OPEN, kernel)

        cv2.imshow("Foreground", mask)

        # Actividad
        white_pixels = cv2.countNonZero(mask)
        activity = white_pixels / mask.size

        # Keyframes
        if index >= warmup and index % step == 0:
            if activity > 0.02:
                cv2.imwrite(
                    f"keyframes/frame_{index:04d}.jpg", frame)

        # Video resumido
        if index >= warmup and activity > 0.02:
            writer.write(frame)

        # Dense Flow
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            previous, gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0)

        dx = flow[:, :, 0]
        dy = flow[:, :, 1]

        # Flow Magnitude
        magnitude = np.sqrt(dx**2 + dy**2)

        # Visualización del movimiento
        motion = np.uint8(
            np.clip(magnitude / 5, 0, 1) * 255)

        cv2.imshow("Motion magnitude", motion)

        # Actualizar frame anterior
        previous = gray

        # Personal: registrar actividad
        activity_vector.append(round(100 * activity, 1))

        print(round(100 * activity, 1), "%")

        index += 1

        # Leer siguiente frame
        ok, frame = cap.read()

        if not ok:
            break

# Promedio de actividad
# print(activity_vector)

promedio = np.mean(activity_vector)
print(f"El promedio es: {round(promedio, 1)}%")

cap.release()
writer.release()
cv2.destroyAllWindows()

# para la siguiente clase poner los the sparse flow result en donde se vea las flechitas a donde va el siguiente movimiento