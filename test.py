import cv2

# Intenta abrir la cámara (0 es la cámara por defecto)
camera = cv2.VideoCapture(0)

# Verifica si la cámara se abrió correctamente
if not camera.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

print("Cámara abierta correctamente. Presiona 'q' para salir.")

# Bucle para capturar y mostrar video
while True:
    # Captura un fotograma
    ret, frame = camera.read()

    # Si no se pudo capturar el fotograma, sal del bucle
    if not ret:
        print("Error: No se pudo capturar el fotograma.")
        break

    # Muestra el fotograma en una ventana
    cv2.imshow("Cámara", frame)

    # Espera 1 ms y verifica si se presionó la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
camera.release()
cv2.destroyAllWindows()
print("Cámara liberada y ventana cerrada.")