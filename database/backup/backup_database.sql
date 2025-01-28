/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.6.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: bioharvestdb
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `bitacora`
--

DROP TABLE IF EXISTS `bitacora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bitacora` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `temperatura` double NOT NULL,
  `ph` double NOT NULL,
  `value_R` double NOT NULL,
  `value_G` double NOT NULL,
  `value_B` double NOT NULL,
  `value_I` double NOT NULL,
  `photo_src` varchar(255) NOT NULL,
  `densidad_celular` double NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora`
--

LOCK TABLES `bitacora` WRITE;
/*!40000 ALTER TABLE `bitacora` DISABLE KEYS */;
INSERT INTO `bitacora` VALUES
(1,25.3,7.4,100,150,200,50,'photos/2025/01/28/photo_20250128_143500.jpg',1.23,'2025-01-28 14:35:00'),
(2,25.3,7.4,100,150,200,50,'photos/2025/01/28/photo_20250128_144500.jpg',1.23,'2025-01-28 14:45:00'),
(3,25.3,7.4,35.761312,32.316416,34.419488,33.400272,'photos/2025/01/28/photo_20250128_144700.jpg',1.23,'2025-01-28 14:47:00'),
(4,25.3,7.4,240.404656,243.88384,246.53216,244.467312,'photos/2025/01/28/photo_20250128_145000.jpg',1.23,'2025-01-28 14:50:00'),
(5,25.3,7.4,230.421536,227.968272,221.444816,226.398224,'photos/2025/01/28/photo_20250128_145100.jpg',1.23,'2025-01-28 14:51:00'),
(6,25.3,7.4,17.164352,25.06464,29.281824,25.362,'photos/2025/01/28/photo_20250128_150600.jpg',1.23,'2025-01-28 15:06:00'),
(7,25.3,7.4,35.088752,39.766768,44.572944,40.661568,'photos/2025/01/28/photo_20250128_150700.jpg',1.23,'2025-01-28 15:07:00'),
(8,25.3,7.4,40.741888,45.159888,49.210608,45.863184,'photos/2025/01/28/photo_20250128_150900.jpg',1.23,'2025-01-28 15:09:00'),
(9,25.3,7.4,47.756816,52.077824,58.909008,53.630192,'photos/2025/01/28/photo_20250128_151000.jpg',1.23,'2025-01-28 15:10:00'),
(10,25.3,7.4,27.332512,30.409296,31.6528,30.414048,'photos/2025/01/28/photo_20250128_151200.jpg',0,'2025-01-28 15:12:00');
/*!40000 ALTER TABLE `bitacora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estimacion_densidad`
--

DROP TABLE IF EXISTS `estimacion_densidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `estimacion_densidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_bitacora` int(11) NOT NULL,
  `densidad_celular` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_bitacora` (`id_bitacora`),
  CONSTRAINT `estimacion_densidad_ibfk_1` FOREIGN KEY (`id_bitacora`) REFERENCES `bitacora` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estimacion_densidad`
--

LOCK TABLES `estimacion_densidad` WRITE;
/*!40000 ALTER TABLE `estimacion_densidad` DISABLE KEYS */;
/*!40000 ALTER TABLE `estimacion_densidad` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-01-28 15:12:00
