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
  `lectura_id` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora`
--

LOCK TABLES `bitacora` WRITE;
/*!40000 ALTER TABLE `bitacora` DISABLE KEYS */;
INSERT INTO `bitacora` VALUES
(32,25.3,7.4,113.170448,125.626864,125.232128,124.11744,'photos/2025/01/30/photo_20250130_095600.jpg',0,'2025-01-30 09:56:00',1,NULL),
(33,25.3,7.4,50.62264,57.763952,66.761904,59.657328,'photos/2025/01/30/photo_20250130_100000.jpg',0,'2025-01-30 10:00:00',2,NULL),
(34,19.05,6.27,45.25888,46.220848,47.902528,46.63008,'photos/2025/01/30/photo_20250130_135400.jpg',0,'2025-01-30 13:54:03',1,NULL),
(35,19.05,6.27,14.147152,13.19056,15.170688,13.913536,'photos/2025/01/30/photo_20250130_141200.jpg',0,'2025-01-30 14:12:03',1,'Test'),
(36,19.05,6.27,48.718368,48.579424,57.01024,51.103152,'photos/2025/01/30/photo_20250130_142200.jpg',0,'2025-01-30 14:22:03',15,'Test'),
(37,19.05,6.27,22.631184,25.154784,27.169024,25.43032,'photos/2025/01/30/photo_20250130_142300.jpg',0,'2025-01-30 14:23:03',14,'Test'),
(38,19.05,6.27,80.322192,82.336992,88.648224,84.007728,'photos/2025/01/30/photo_20250130_144200.jpg',0,'2025-01-30 14:42:03',14,'Test'),
(39,21.3125,4.290235,13.909008,18.36832,27.097728,20.426896,'photos/2025/01/31/photo_20250131_084325.jpg',0,'2025-01-31 08:43:34',1,'Test'),
(40,19.5625,7.232943,55.056912,64.339312,82.984,68.830768,'photos/2025/01/31/photo_20250131_100856.jpg',0,'2025-01-31 10:09:07',0,'NaN');
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

-- Dump completed on 2025-02-03 10:55:01
