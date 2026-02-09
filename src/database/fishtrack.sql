CREATE DATABASE `fishtrack`;
USE `fishtrack`;

-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: fishtrack
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `fishcast`
--

DROP TABLE IF EXISTS `fishcast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishcast` (
  `ID` varchar(32) NOT NULL,
  `KEY` varchar(32) NOT NULL,
  `BATCH` datetime(6) NOT NULL,
  PRIMARY KEY (`KEY`),
  KEY `fk_ID1` (`ID`),
  CONSTRAINT `fk_ID1` FOREIGN KEY (`ID`) REFERENCES `fishlist` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishcast`
--

LOCK TABLES `fishcast` WRITE;
/*!40000 ALTER TABLE `fishcast` DISABLE KEYS */;
INSERT INTO `fishcast` VALUES ('03c7c0ace395d80182db07ae2c30f034','008b04c539678747a695249bc20dc43c','2026-02-04 04:28:15.887741'),('d41d8cd98f00b204e9800998ecf8427e','0eeca1160aaaa5896ef1c10d541dd545','2026-02-04 04:50:41.173856'),('21e372b3d86c4731e8f5a8cc20e0c904','18e9e07a2406181c5843053d2b56d60c','2026-02-03 08:48:35.588354'),('2326c7e8efb1f97e6d47c16d22a7a6f4','1bbf1c1e56f462fb81e178e0c2ac1efc','2026-02-04 04:19:27.760626'),('d41d8cd98f00b204e9800998ecf8427e','2f99cfca5b3f95670118fad3c2b866ec','2026-02-04 04:43:22.018599'),('2326c7e8efb1f97e6d47c16d22a7a6f4','2fa03db6b5c2592ac2d7a4baa4dbf405','2026-02-04 04:31:43.972811'),('2326c7e8efb1f97e6d47c16d22a7a6f4','3b86c4348d841cf7aea71f37a93025c4','2026-02-03 08:39:48.996587'),('03c7c0ace395d80182db07ae2c30f034','3c31727f4d877fe84c96828734d5ce35','2026-02-04 04:14:29.122007'),('03c7c0ace395d80182db07ae2c30f034','404d91b4a1a4cf31b219149413fa80d5','2026-02-04 04:33:28.834913'),('1679091c5a880faf6fb5e6087eb1b2dc','521205c244b5249f377c9bb835b62f0f','2026-02-04 04:16:09.882566'),('03c7c0ace395d80182db07ae2c30f034','62d78b63e972d9e29a1e82e761cea49e','2026-02-04 04:41:42.068843'),('14c959cd94a0be28dc8c2f7d834d1316','6d83c22736fb25ba38db952449b2cd1e','2026-02-04 04:50:41.173856'),('21e372b3d86c4731e8f5a8cc20e0c904','6de78c9512f2ee5072d1016e063472a6','2026-02-03 08:39:48.996587'),('2326c7e8efb1f97e6d47c16d22a7a6f4','728474dc19e5ceaf3fb1086bc9327793','2026-02-03 08:48:35.588354'),('03c7c0ace395d80182db07ae2c30f034','87ff3044790963a5d069d6e065b2c88d','2026-02-04 04:16:56.805236'),('03c7c0ace395d80182db07ae2c30f034','88899586f9e65ea15969cd0c22cac70d','2026-02-04 04:39:59.873572'),('03c7c0ace395d80182db07ae2c30f034','903c8a28ccc35bbaa0895c212d34ef33','2026-02-04 04:21:17.024408'),('03c7c0ace395d80182db07ae2c30f034','95c70f88d47707f9efdb64a4150ea5cb','2026-02-04 04:13:33.135499'),('21e372b3d86c4731e8f5a8cc20e0c904','96afecae2ea61d3960d712c302bc4c68','2026-02-04 06:40:41.038750'),('2326c7e8efb1f97e6d47c16d22a7a6f4','96d7c8f1c3da20c7e86b21a3dd157d2f','2026-02-04 06:40:41.038750'),('21e372b3d86c4731e8f5a8cc20e0c904','9f544bef82e804ba0c30da1049b772f6','2026-02-04 04:19:27.760626'),('14c959cd94a0be28dc8c2f7d834d1316','c7e0896ce1b918a20b88d7c6f0040610','2026-02-04 06:40:41.038750'),('14c959cd94a0be28dc8c2f7d834d1316','c8ff9b48f4816dc3cd1d037639fe3751','2026-02-04 04:43:22.018599'),('21e372b3d86c4731e8f5a8cc20e0c904','e2a01c321629574e2ba5bed5c52d496d','2026-02-04 04:31:43.972811');
/*!40000 ALTER TABLE `fishcast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fishcook`
--

DROP TABLE IF EXISTS `fishcook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishcook` (
  `ID` varchar(32) NOT NULL,
  `KEY` varchar(32) NOT NULL,
  `PWND` datetime NOT NULL,
  `TEXT` varchar(64) DEFAULT NULL,
  KEY `fk_key2` (`KEY`),
  KEY `fk_ID3` (`ID`),
  CONSTRAINT `fk_ID3` FOREIGN KEY (`ID`) REFERENCES `fishlist` (`ID`),
  CONSTRAINT `fk_key2` FOREIGN KEY (`KEY`) REFERENCES `fishcast` (`KEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishcook`
--

LOCK TABLES `fishcook` WRITE;
/*!40000 ALTER TABLE `fishcook` DISABLE KEYS */;
INSERT INTO `fishcook` VALUES ('2326c7e8efb1f97e6d47c16d22a7a6f4','728474dc19e5ceaf3fb1086bc9327793','2026-02-04 03:09:09','password'),('21e372b3d86c4731e8f5a8cc20e0c904','18e9e07a2406181c5843053d2b56d60c','2026-02-04 10:17:11','realpassword');
/*!40000 ALTER TABLE `fishcook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fishhook`
--

DROP TABLE IF EXISTS `fishhook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishhook` (
  `ID` varchar(32) NOT NULL,
  `KEY` varchar(32) NOT NULL,
  `CLICK` datetime NOT NULL,
  KEY `fk_key1` (`KEY`),
  KEY `fk_ID2` (`ID`),
  CONSTRAINT `fk_ID2` FOREIGN KEY (`ID`) REFERENCES `fishlist` (`ID`),
  CONSTRAINT `fk_key1` FOREIGN KEY (`KEY`) REFERENCES `fishcast` (`KEY`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishhook`
--

LOCK TABLES `fishhook` WRITE;
/*!40000 ALTER TABLE `fishhook` DISABLE KEYS */;
INSERT INTO `fishhook` VALUES ('2326c7e8efb1f97e6d47c16d22a7a6f4','728474dc19e5ceaf3fb1086bc9327793','2026-02-04 02:45:01'),('2326c7e8efb1f97e6d47c16d22a7a6f4','728474dc19e5ceaf3fb1086bc9327793','2026-02-04 02:59:41'),('21e372b3d86c4731e8f5a8cc20e0c904','18e9e07a2406181c5843053d2b56d60c','2026-02-04 10:16:26'),('14c959cd94a0be28dc8c2f7d834d1316','c8ff9b48f4816dc3cd1d037639fe3751','2026-02-04 11:45:10'),('14c959cd94a0be28dc8c2f7d834d1316','6d83c22736fb25ba38db952449b2cd1e','2026-02-04 11:55:55');
/*!40000 ALTER TABLE `fishhook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fishlist`
--

DROP TABLE IF EXISTS `fishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fishlist` (
  `ID` varchar(32) NOT NULL,
  `EMAIL` varchar(64) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fishlist`
--

LOCK TABLES `fishlist` WRITE;
/*!40000 ALTER TABLE `fishlist` DISABLE KEYS */;
INSERT INTO `fishlist` VALUES ('03c7c0ace395d80182db07ae2c30f034','s'),('14c959cd94a0be28dc8c2f7d834d1316','siwapon.so11@gmail.com'),('1679091c5a880faf6fb5e6087eb1b2dc','6'),('21e372b3d86c4731e8f5a8cc20e0c904','siwanon.trairattana@gmail.com'),('2326c7e8efb1f97e6d47c16d22a7a6f4','siwaaltmail@gmail.com'),('d41d8cd98f00b204e9800998ecf8427e','');
/*!40000 ALTER TABLE `fishlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-04  6:48:06
