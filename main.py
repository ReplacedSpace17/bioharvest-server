from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import os
import cv2
import pymysql  # Librería para conectar a MySQL
import numpy as np
import subprocess  # Para ejecutar comandos del sistema
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # Importar CORSMiddleware
import serial
import json
import time

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    "host": "localhost",
    "user": "pythondb",
    "password": "Javier117",
    "database": "bioharvestdb",
}
connection = pymysql.connect(**DB_CONFIG)
NombreExp = os.getenv('NAME_EXPERIMENT', 'NaN')
# Crear una instancia de la aplicación FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (puedes especificar una lista de dominios si lo deseas)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)

# Montar el directorio donde se encuentra la carpeta dist
app.mount("/static", StaticFiles(directory="panel/dist"), name="static")





# Ruta de ejemplo
@app.get("/")
async def read_index():
    return FileResponse("panel/dist/index.html")

@app.get("/take_photo")
async def take_photo_endpoint():
    try:
        filepath = take_photo()
        return {"message": "Foto tomada correctamente", "path": filepath}
    except RuntimeError as e:
        return {"error": str(e)}

# Endpoint para probar el serveer
@app.get("/test")
async def test_status():
    if scheduler.running:
        return JSONResponse(content={"status": "El servidor está funcionando correctamente y el programador de tareas está activo."}, status_code=200)
    else:
        return JSONResponse(content={"status": "El servidor está funcionando, pero el programador de tareas no está activo."}, status_code=200)

# Endpoint para obtener las estadisticas
@app.get("/statistic")
async def get_statistics():
    try:
        # Conectar a la base de datos
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # Ejecutar la consulta SELECT
            cursor.execute("SELECT * FROM bitacora")
            # Obtener todos los resultados
            rows = cursor.fetchall()
            
            # Preparar los resultados como una lista de diccionarios
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]
            
            # Convertir objetos datetime a formato string
            for result in results:
                for key, value in result.items():
                    if isinstance(value, datetime):
                        result[key] = value.isoformat()  # Convierte el datetime a ISO 8601
            
            # Retornar los resultados en formato JSON
            return JSONResponse(content={"statistics": results}, status_code=200)
    except pymysql.MySQLError as e:
        # Si ocurre un error, retorna un mensaje de error
        return JSONResponse(content={"error": f"Error al acceder a la base de datos: {e}"}, status_code=500)
    finally:
        # Cerrar la conexión
        connection.close()

# Endpoint para obtener las fotos (photo_src y date)
@app.get("/getPhotos")
async def get_photos():
    try:
        # Conectar a la base de datos
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # Ejecutar la consulta SELECT
            cursor.execute("SELECT photo_src, date FROM bitacora")
            # Obtener todos los resultados
            rows = cursor.fetchall()

            # Preparar los resultados como una lista de diccionarios
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in rows]
            
            # Convertir objetos datetime a formato string
            for result in results:
                result["date"] = result["date"].strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha

            # Retornar los resultados en formato JSON
            return JSONResponse(content={"photos": results}, status_code=200)
    except pymysql.MySQLError as e:
        # Si ocurre un error, retorna un mensaje de error
        return JSONResponse(content={"error": f"Error al acceder a la base de datos: {e}"}, status_code=500)
    finally:
        # Cerrar la conexión
        connection.close()

@app.get("/view/{file_path:path}")
async def view_image(file_path: str):
    file_path_full = os.path.join(PHOTO_DIR, file_path)
    print(f"Ruta completa: {file_path_full}")  # Esto te ayudará a verificar la ruta real
    
    if os.path.exists(file_path_full):
        return FileResponse(file_path_full)
    else:
        return {"error": f"Archivo no encontrado: {file_path_full}"}

# ------------------------------------------------------------------------------- Funciones
def obtener_datos_arduino():
    # Obtener el puerto serie desde la variable de entorno ARDUINO_PORT
    puerto_serie = os.getenv('ARDUINO_PORT', '/dev/ttyACM0')  # Si no está configurado, usa '/dev/ttyUSB0' por defecto
    baudios = 9600  # Cambia esto por la tasa de baudios que utiliza tu Arduino

    # Inicia la conexión serial
    ser = serial.Serial(puerto_serie, baudios, timeout=1)  
    time.sleep(10)  # Espera a que Arduino inicie

    # Enviar el comando 'd' para solicitar datos
    ser.write(b"d\n")

    # Leer la respuesta de Arduino
    respuesta = ser.readline().decode().strip()

    # Intentamos convertir la respuesta a JSON (esto debería ser un objeto JSON como {"t": 19.05, "ph": 6.27})
    try:
        datos = json.loads(respuesta)
        temperatura = datos.get('t', None)  # Obtener la temperatura 't' (si existe)
        ph = datos.get('ph', None)  # Obtener el pH (si existe)
        
        # Imprimir los valores obtenidos
        #print(f"Temperatura: {temperatura}°C, pH: {ph}")

        # Regresar los valores
        return temperatura, ph
    
    except json.JSONDecodeError:
        print("Error al recibir datos de Arduino. La respuesta no es un JSON válido.")
        return None, None

    finally:
        # Cerrar la conexión
        ser.close()

# Función de ejemplo
def print_hello_world():
    print(f"{datetime.now()} - Hello World")

# Directorio donde se guardarán las fotos
PHOTO_DIR = "photos"
# Servir archivos estáticos desde el directorio de fotos
app.mount("/photos", StaticFiles(directory=PHOTO_DIR), name="photos")
os.makedirs(PHOTO_DIR, exist_ok=True)


def take_photo():
    # Inicializa la cámara (0 para la cámara por defecto)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Error: No se pudo acceder a la cámara.")

    # Intenta capturar un fotograma varias veces
    ret = False
    for _ in range(10):  # Intenta 10 veces
        ret, frame = camera.read()
        if ret:
            break
        time.sleep(0.1)  # Espera 100 ms antes de intentar de nuevo

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

def save_to_database(temp, ph, r, g, b, i, filepath, densidad_celular, lectura_id):
    """
    Inserta los datos en la tabla bitacora.
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            query = """
                INSERT INTO bitacora (temperatura, ph, value_R, value_G, value_B, value_I, photo_src, densidad_celular, date, lectura_id, nombre)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()        
            cursor.execute(query, (temp, ph, r, g, b, i, filepath, densidad_celular, now, lectura_id, NombreExp))
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
def iniciar_aplicacion(lectura_id):
    try:
        print("Corriendo la aplicación")
        # Toma la foto y obtiene la ruta del archivo
        filepath = take_photo()
        #Procesar la imagen
        red_avg, green_avg, blue_avg, intensity_avg = procesing_image(filepath)

        # Simula una lectura de temperatura y pH desde un sensor
        temp, ph = obtener_datos_arduino()
        print(f"Temperatura: {temp} °C, pH: {ph}")
        # Valores de los promedios de las bandas
        r=red_avg
        g=green_avg
        b=blue_avg
        i=intensity_avg

        #calcular la densidad celular PENDIENTE
        densidad_celular=0.0


        # Guarda los datos en la base de datos
        save_to_database(temp, ph, r, g, b, i, filepath, densidad_celular, lectura_id)
        # Realiza un respaldo de la base de datos
        backup_database()
    except Exception as e:
        print(f"Error en la aplicación principal: {e}")

# Configurar el programador de tareas para registro en bitacora
scheduler = BackgroundScheduler()
scheduler.add_job(iniciar_aplicacion, 'date', run_date=datetime.now() + timedelta(seconds=10), args=[0])

for hora in range(24):
    scheduler.add_job(iniciar_aplicacion, 'cron', hour=hora, minute=00, args=[hora])
scheduler.start()

# Cerrar el programador al apagar la aplicación
@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()
