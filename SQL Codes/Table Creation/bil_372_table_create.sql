CREATE DATABASE  IF NOT EXISTS `bil372_project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bil372_project`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: bil372_project
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `KullanıcıID` int NOT NULL,
  PRIMARY KEY (`KullanıcıID`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`KullanıcıID`) REFERENCES `kullanıcı` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hastahayvan`
--

DROP TABLE IF EXISTS `hastahayvan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hastahayvan` (
  `HastaID` int NOT NULL,
  `SahipID` int NOT NULL,
  `Yaş` int DEFAULT NULL,
  `Boy` int DEFAULT NULL,
  `İsim` varchar(100) DEFAULT NULL,
  `Kilo` double DEFAULT NULL,
  PRIMARY KEY (`SahipID`,`HastaID`),
  KEY `idx_hastaid` (`HastaID`),
  CONSTRAINT `hastahayvan_ibfk_1` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hastahayvan`
--

LOCK TABLES `hastahayvan` WRITE;
/*!40000 ALTER TABLE `hastahayvan` DISABLE KEYS */;
/*!40000 ALTER TABLE `hastahayvan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hayvansahibi`
--

DROP TABLE IF EXISTS `hayvansahibi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hayvansahibi` (
  `KullanıcıID` int NOT NULL,
  `İsim` varchar(255) DEFAULT NULL,
  `Soyisim` varchar(255) DEFAULT NULL,
  `İl` varchar(255) DEFAULT NULL,
  `İlçe` varchar(255) DEFAULT NULL,
  `Mahalle` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`KullanıcıID`),
  CONSTRAINT `hayvansahibi_ibfk_1` FOREIGN KEY (`KullanıcıID`) REFERENCES `kullanıcı` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hayvansahibi`
--

LOCK TABLES `hayvansahibi` WRITE;
/*!40000 ALTER TABLE `hayvansahibi` DISABLE KEYS */;
/*!40000 ALTER TABLE `hayvansahibi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ilaçlar`
--

DROP TABLE IF EXISTS `ilaçlar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ilaçlar` (
  `İlaçID` int NOT NULL AUTO_INCREMENT,
  `İsim` varchar(255) DEFAULT NULL,
  `Fiyat` varchar(255) DEFAULT NULL,
  `Miktar` varchar(255) DEFAULT NULL,
  `AdminID` int DEFAULT NULL,
  PRIMARY KEY (`İlaçID`),
  KEY `AdminID` (`AdminID`),
  CONSTRAINT `ilaçlar_ibfk_1` FOREIGN KEY (`AdminID`) REFERENCES `admin` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ilaçlar`
--

LOCK TABLES `ilaçlar` WRITE;
/*!40000 ALTER TABLE `ilaçlar` DISABLE KEYS */;
/*!40000 ALTER TABLE `ilaçlar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `içerir`
--

DROP TABLE IF EXISTS `içerir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `içerir` (
  `İlaçID` int NOT NULL,
  `ReçeteID` int NOT NULL,
  PRIMARY KEY (`İlaçID`,`ReçeteID`),
  KEY `ReçeteID` (`ReçeteID`),
  CONSTRAINT `içerir_ibfk_1` FOREIGN KEY (`İlaçID`) REFERENCES `ilaçlar` (`İlaçID`),
  CONSTRAINT `içerir_ibfk_2` FOREIGN KEY (`ReçeteID`) REFERENCES `reçete` (`ReçeteID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `içerir`
--

LOCK TABLES `içerir` WRITE;
/*!40000 ALTER TABLE `içerir` DISABLE KEYS */;
/*!40000 ALTER TABLE `içerir` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kullanıcı`
--

DROP TABLE IF EXISTS `kullanıcı`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kullanıcı` (
  `KullanıcıID` int NOT NULL AUTO_INCREMENT,
  `Email` varchar(100) DEFAULT NULL,
  `Şifre` varchar(50) DEFAULT NULL,
  `Rol` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kullanıcı`
--

LOCK TABLES `kullanıcı` WRITE;
/*!40000 ALTER TABLE `kullanıcı` DISABLE KEYS */;
/*!40000 ALTER TABLE `kullanıcı` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `muayenefaturası`
--

DROP TABLE IF EXISTS `muayenefaturası`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `muayenefaturası` (
  `FaturaID` int NOT NULL AUTO_INCREMENT,
  `SahipID` int NOT NULL,
  `Ücret` double DEFAULT NULL,
  PRIMARY KEY (`FaturaID`,`SahipID`),
  KEY `SahipID` (`SahipID`),
  CONSTRAINT `muayenefaturası_ibfk_1` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muayenefaturası`
--

LOCK TABLES `muayenefaturası` WRITE;
/*!40000 ALTER TABLE `muayenefaturası` DISABLE KEYS */;
/*!40000 ALTER TABLE `muayenefaturası` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `randevu`
--

DROP TABLE IF EXISTS `randevu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `randevu` (
  `RandevuID` int NOT NULL AUTO_INCREMENT,
  `Gün` varchar(255) DEFAULT NULL,
  `Saat` varchar(255) DEFAULT NULL,
  `SahipID` int DEFAULT NULL,
  PRIMARY KEY (`RandevuID`),
  KEY `SahipID` (`SahipID`),
  CONSTRAINT `randevu_ibfk_1` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `randevu`
--

LOCK TABLES `randevu` WRITE;
/*!40000 ALTER TABLE `randevu` DISABLE KEYS */;
/*!40000 ALTER TABLE `randevu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `renkler`
--

DROP TABLE IF EXISTS `renkler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `renkler` (
  `HayvanID` int NOT NULL,
  `Renk` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`HayvanID`),
  CONSTRAINT `renkler_ibfk_1` FOREIGN KEY (`HayvanID`) REFERENCES `hastahayvan` (`HastaID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renkler`
--

LOCK TABLES `renkler` WRITE;
/*!40000 ALTER TABLE `renkler` DISABLE KEYS */;
/*!40000 ALTER TABLE `renkler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviewverir`
--

DROP TABLE IF EXISTS `reviewverir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviewverir` (
  `HayvanSahibiID` int NOT NULL,
  `VeterinerID` int NOT NULL,
  `Açıklama` varchar(255) NOT NULL,
  `Puan` int NOT NULL,
  PRIMARY KEY (`HayvanSahibiID`,`VeterinerID`),
  KEY `VeterinerID` (`VeterinerID`),
  CONSTRAINT `reviewverir_ibfk_1` FOREIGN KEY (`HayvanSahibiID`) REFERENCES `hayvansahibi` (`KullanıcıID`),
  CONSTRAINT `reviewverir_ibfk_2` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviewverir`
--

LOCK TABLES `reviewverir` WRITE;
/*!40000 ALTER TABLE `reviewverir` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviewverir` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reçete`
--

DROP TABLE IF EXISTS `reçete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reçete` (
  `ReçeteID` int NOT NULL AUTO_INCREMENT,
  `Tarih` varchar(255) DEFAULT NULL,
  `VeterinerID` int DEFAULT NULL,
  `HastaHayvanID` int NOT NULL,
  PRIMARY KEY (`ReçeteID`),
  KEY `VeterinerID` (`VeterinerID`),
  KEY `HastaHayvanID` (`HastaHayvanID`),
  CONSTRAINT `reçete_ibfk_1` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`),
  CONSTRAINT `reçete_ibfk_2` FOREIGN KEY (`HastaHayvanID`) REFERENCES `hastahayvan` (`HastaID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reçete`
--

LOCK TABLES `reçete` WRITE;
/*!40000 ALTER TABLE `reçete` DISABLE KEYS */;
/*!40000 ALTER TABLE `reçete` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verir`
--

DROP TABLE IF EXISTS `verir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verir` (
  `RandevuID` int NOT NULL,
  `VeterinerID` int NOT NULL,
  PRIMARY KEY (`RandevuID`,`VeterinerID`),
  KEY `VeterinerID` (`VeterinerID`),
  CONSTRAINT `verir_ibfk_1` FOREIGN KEY (`RandevuID`) REFERENCES `randevu` (`RandevuID`),
  CONSTRAINT `verir_ibfk_2` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verir`
--

LOCK TABLES `verir` WRITE;
/*!40000 ALTER TABLE `verir` DISABLE KEYS */;
/*!40000 ALTER TABLE `verir` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veteriner`
--

DROP TABLE IF EXISTS `veteriner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `veteriner` (
  `KullanıcıID` int NOT NULL,
  `İsim` varchar(255) DEFAULT NULL,
  `Soyisim` varchar(255) DEFAULT NULL,
  `TCNO` varchar(11) DEFAULT NULL,
  `TelefonNo` varchar(11) DEFAULT NULL,
  `İlçe` varchar(255) DEFAULT NULL,
  `Mahalle` varchar(255) DEFAULT NULL,
  `İl` varchar(255) DEFAULT NULL,
  `OdaNO` int DEFAULT NULL,
  `AdminID` int NOT NULL,
  PRIMARY KEY (`KullanıcıID`),
  KEY `AdminID` (`AdminID`),
  CONSTRAINT `veteriner_ibfk_1` FOREIGN KEY (`KullanıcıID`) REFERENCES `kullanıcı` (`KullanıcıID`),
  CONSTRAINT `veteriner_ibfk_2` FOREIGN KEY (`AdminID`) REFERENCES `admin` (`KullanıcıID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veteriner`
--

LOCK TABLES `veteriner` WRITE;
/*!40000 ALTER TABLE `veteriner` DISABLE KEYS */;
/*!40000 ALTER TABLE `veteriner` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-07 12:35:40
