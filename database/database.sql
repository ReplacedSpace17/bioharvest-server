CREATE DATABASE bioharvestdb;
USE bioharvestdb;
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

CREATE TABLE estimacion_densidad (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_bitacora INT NOT NULL,          -- ID relacionado con la tabla bitacora
    densidad_celular DOUBLE NOT NULL,  -- Densidad celular estimada
    FOREIGN KEY (id_bitacora) REFERENCES bitacora(id) ON DELETE CASCADE
);
