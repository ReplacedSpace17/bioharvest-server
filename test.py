import serial
import time
import json
import os

def obtener_datos_arduino():
    # Obtener el puerto serie desde la variable de entorno ARDUINO_PORT
    puerto_serie = os.getenv('ARDUINO_PORT', '/dev/ttyACM0')  # Si no está configurado, usa '/dev/ttyUSB0' por defecto
    baudios = 9600  # Cambia esto por la tasa de baudios que utiliza tu Arduino

    # Inicia la conexión serial
    ser = serial.Serial(puerto_serie, baudios, timeout=1)  
    time.sleep(3)  # Espera a que Arduino inicie

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
        print(f"Temperatura: {temperatura}°C, pH: {ph}")

        # Regresar los valores
        return temperatura, ph
    
    except json.JSONDecodeError:
        print("Error al recibir datos de Arduino. La respuesta no es un JSON válido.")
        return None, None

    finally:
        # Cerrar la conexión
        ser.close()

# Ejemplo de uso de la función
temperatura, ph = obtener_datos_arduino()
