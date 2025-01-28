from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import cv2
import pymysql  # Librería para conectar a MySQL
import numpy as np
import subprocess  # Para ejecutar comandos del sistema

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

#Ip del arduino
IP_ARDUINO = "192.1.168.12"

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "pythondb",
    "password": "Javier117",
    "database": "bioharvestdb",
}

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

# ------------------------------------------------------------------------------- Funciones

# Función de ejemplo
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

def save_to_database(temp, ph, r, g, b, i, filepath, densidad_celular):
    """
    Inserta los datos en la tabla bitacora.
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            query = """
                INSERT INTO bitacora (temperatura, ph, value_R, value_G, value_B, value_I, photo_src, densidad_celular, date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()        
            cursor.execute(query, (temp, ph, r, g, b, i, filepath, densidad_celular, now))
            connection.commit()
            print(f"{datetime.now()} - Datos guardados en la base de datos.")
    except pymysql.MySQLError as e:
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        connection.close()

def procesing_image(filepath):
    # Leer la imagen desde el filepath
    image = cv2.imread(filepath)
    if image is None:
        raise ValueError(f"No se pudo cargar la imagen desde {filepath}")
    
    # Convertir la imagen a formato RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Definir las coordenadas de la ROI (centrada en la imagen, 250x250 píxeles)
    height, width = image.shape[:2]
    roi_x = int((width - 250) / 2)
    roi_y = int((height - 250) / 2)
    roi_width = 250
    roi_height = 250
    
    # Extraer la ROI
    roi = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    
    # Separar las bandas RGB
    blue_channel, green_channel, red_channel = cv2.split(roi)
    
    # Calcular la banda de intensidad (I)
    intensity_channel = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    
    # Calcular los promedios de cada banda
    blue_avg = np.mean(blue_channel)
    green_avg = np.mean(green_channel)
    red_avg = np.mean(red_channel)
    intensity_avg = np.mean(intensity_channel)
    
    # Devolver los promedios de las bandas
    return red_avg, green_avg, blue_avg, intensity_avg

BACKUP_DIR = "database/backup"
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_database():
    """
    Realiza un respaldo de la base de datos y lo guarda en la carpeta de respaldo.
    """
    try:
        now = datetime.now()
        filename = f"backup_database.sql"
        filepath = os.path.join(BACKUP_DIR, filename)

        # Comando mysqldump para realizar el respaldo
        command = [
            "mysqldump",
            "-h", DB_CONFIG["host"],
            "-u", DB_CONFIG["user"],
            f"--password={DB_CONFIG['password']}",
            DB_CONFIG["database"],
            "-r", filepath
        ]

        # Ejecutar el comando
        subprocess.run(command, check=True)
        print(f"{datetime.now()} - Respaldo creado exitosamente en {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Error al crear el respaldo de la base de datos: {e}")

# Función principal
def iniciar_aplicacion():
    try:
        print("Corriendo la aplicación")
        # Toma la foto y obtiene la ruta del archivo
        filepath = take_photo()
        #Procesar la imagen
        red_avg, green_avg, blue_avg, intensity_avg = procesing_image(filepath)

        # Simula una lectura de temperatura y pH desde un sensor
        #Request al arduino para obtener la temperatura y el ph
        
        temp = 25.3
        ph = 7.4
        # Valores de los promedios de las bandas
        r=red_avg
        g=green_avg
        b=blue_avg
        i=intensity_avg

        #calcular la densidad celular PENDIENTE
        densidad_celular=0.0


        # Guarda los datos en la base de datos
        save_to_database(temp, ph, r, g, b, i, filepath, densidad_celular)
        # Realiza un respaldo de la base de datos
        backup_database()
    except Exception as e:
        print(f"Error en la aplicación principal: {e}")

# Configurar el programador de tareas para registro en bitacora
scheduler = BackgroundScheduler()
scheduler.add_job(iniciar_aplicacion, 'cron', hour=15, minute=12)  # Programa la tarea a las 10:44 AM
scheduler.start()

# Cerrar el programador al apagar la aplicación
@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
