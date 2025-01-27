from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import cv2

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Ruta de ejemplo
@app.get("/")
async def read_root():
    return {"message": "¡Servidor HTTP en FastAPI funcionando correctamente!"}

@app.get("/take_photo")
async def take_photo_endpoint():
    try:
        filepath = take_photo()
        return {"message": "Foto tomada correctamente", "path": filepath}
    except RuntimeError as e:
        return {"error": str(e)}
#-------------------------------------------------------------------------------  Funciónes

#Funcion de ejemplo
def print_hello_world():
    print(f"{datetime.now()} - Hello World")

# Directorio donde se guardarán las fotos
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

def take_photo():
    # Inicializa la cámara (0 para la cámara por defecto)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Error: No se pudo acceder a la cámara.")

    # Captura un fotograma
    ret, frame = camera.read()

    if not ret:
        camera.release()
        raise RuntimeError("Error: No se pudo capturar la imagen.")

    # Generar ruta dinámica para guardar la foto
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    # Crear subdirectorios basados en año, mes y día
    subdir = os.path.join(PHOTO_DIR, year, month, day)
    os.makedirs(subdir, exist_ok=True)

    # Nombre completo del archivo
    filename = f"photo_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
    filepath = os.path.join(subdir, filename)

    # Guarda la imagen capturada
    cv2.imwrite(filepath, frame)
    print(f"{datetime.now()} - Foto guardada como {filepath}")

    # Libera la cámara
    camera.release()

    return filepath

# Configurar el programador de tareas para registro en bitacora
scheduler = BackgroundScheduler()
scheduler.add_job(print_hello_world, 'cron', hour=10, minute=44)  # Programa la tarea para las 12:00 PM todos los días
scheduler.start()

# Cerrar el programador al apagar la aplicación
@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
