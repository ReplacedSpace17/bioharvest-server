-- Crear el usuario
CREATE USER 'pythondb'@'localhost' IDENTIFIED BY 'Javier117';

-- Otorgar permisos al usuario para la base de datos bioharvestdb
GRANT ALL PRIVILEGES ON bioharvestdb.* TO 'pythondb'@'localhost';

-- Aplicar los cambios
FLUSH PRIVILEGES;

-- Crear la base de datos
CREATE DATABASE bioharvestdb;

-- Usar la base de datos
USE bioharvestdb;

-- Crear la tabla bitacora
CREATE TABLE bitacora (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperatura DOUBLE NOT NULL,       -- Temperatura de la muestra
    ph DOUBLE NOT NULL,                -- Valor del pH
    value_R DOUBLE NOT NULL,
    value_G DOUBLE NOT NULL,
    value_B DOUBLE NOT NULL,
    value_I DOUBLE NOT NULL,
    photo_src VARCHAR(255) NOT NULL,   -- Ruta de la foto
    densidad_celular DOUBLE NOT NULL,  -- Densidad celular
    date DATETIME NOT NULL             -- Fecha y hora
);

-- Crear la tabla estimacion_densidad
CREATE TABLE estimacion_densidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_bitacora INT NOT NULL,          -- ID relacionado con la tabla bitacora
    densidad_celular DOUBLE NOT NULL,  -- Densidad celular estimada
    FOREIGN KEY (id_bitacora) REFERENCES bitacora(id) ON DELETE CASCADE
);
