# Crear BD
database.sql

# Agregar usuarios
database.sql

# Instalar conda
conda create -n fastapi_env python=3.10
conda activate fastapi_env


# Instalar requeriments.txt
pip install -r requirements.txt

pip freeze > requirements.txt

# Agregar variable de env
nano ~/.bashrc
export ARDUINO_PORT=/dev/ttyUSB0
export NAME_EXPERIMENT=Test
source ~/.bashrc

# Probar
conda activate fastapi_env
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Inicio automatico
conda activate fastapi_env
RUTA_CONDA  = echo $CONDA_PREFIX
USER = echo $USER
GRUPO = id -gn
RUTA_APP = /home/rs17/Documentos/Proyectos/MCC/bioharvest-fotobiorreactor-pc


sudo nano /etc/systemd/system/bioharvest.service
________________________________________
[Unit]
Description=Servicio de BioHarvest (FastAPI con Uvicorn)
After=network.target

[Service]
User=rs17
Group=rs17
WorkingDirectory=/home/rs17/Documentos/Proyectos/MCC/bioharvest-fotobiorreactor-pc
ExecStart=/home/rs17/miniconda3/envs/fastapi_env/bin/uvicorn bioharvest.main:app --host 0.0.0.0 --port 8000 --reload
Restart=always
RestartSec=5s
TimeoutSec=30
LimitNOFILE=65535
Environment="PATH=/home/rs17/miniconda3/envs/fastapi_env/bin:$PATH"
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
________________________________________


sudo systemctl daemon-reload
sudo systemctl enable bioharvest.service
sudo systemctl start bioharvest.service
sudo systemctl status bioharvest.service

# Puerto 8000 backend
# Puerto 9000 panel-react
