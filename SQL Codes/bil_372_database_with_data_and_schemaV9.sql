CREATE DATABASE  IF NOT EXISTS `bil372_project` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bil372_project`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: bil372_project
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `hastahayvan`
--

DROP TABLE IF EXISTS `hastahayvan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hastahayvan` (
  `HastaID` int NOT NULL AUTO_INCREMENT,
  `SahipID` int NOT NULL,
  `Yaş` int DEFAULT NULL,
  `Boy` int DEFAULT NULL,
  `İsim` varchar(100) DEFAULT NULL,
  `Kilo` double DEFAULT NULL,
  `Tür` enum('Kedi','Köpek','Kuş','Tavşan','Kaplumbağa','Hamster','Kobay') NOT NULL,
  `Cinsiyet` enum('Dişi','Erkek') NOT NULL,
  PRIMARY KEY (`SahipID`,`HastaID`),
  KEY `idx_hastaid` (`HastaID`),
  CONSTRAINT `hastahayvan_ibfk_1` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `hayvansahibi_ibfk_1` FOREIGN KEY (`KullanıcıID`) REFERENCES `kullanıcı` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ilaçlar`
--

DROP TABLE IF EXISTS `ilaçlar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ilaçlar` (
  `İlaçID` int NOT NULL AUTO_INCREMENT,
  `İsim` varchar(255) NOT NULL,
  `Fiyat` varchar(255) DEFAULT NULL,
  `Miktar` varchar(255) DEFAULT NULL,
  `AdminID` int NOT NULL,
  PRIMARY KEY (`İlaçID`),
  UNIQUE KEY `İsim` (`İsim`,`AdminID`),
  KEY `AdminID` (`AdminID`),
  CONSTRAINT `ilaçlar_ibfk_1` FOREIGN KEY (`AdminID`) REFERENCES `admin` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `içerir_ibfk_1` FOREIGN KEY (`İlaçID`) REFERENCES `ilaçlar` (`İlaçID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `içerir_ibfk_2` FOREIGN KEY (`ReçeteID`) REFERENCES `reçete` (`ReçeteID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  PRIMARY KEY (`KullanıcıID`),
  UNIQUE KEY `Email` (`Email`),
  CONSTRAINT `kullanıcı_chk_1` CHECK (((`Rol` = _utf8mb3'admin') or (`Rol` = _utf8mb3'veteriner') or (`Rol` = _utf8mb3'kullanıcı')))
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  CONSTRAINT `muayenefaturası_ibfk_1` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `randevu`
--

DROP TABLE IF EXISTS `randevu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `randevu` (
  `VeterinerID` int NOT NULL,
  `SahipID` int NOT NULL,
  `Tarih` datetime NOT NULL,
  PRIMARY KEY (`VeterinerID`,`SahipID`,`Tarih`),
  KEY `SahipID` (`SahipID`),
  CONSTRAINT `randevu_ibfk_1` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`),
  CONSTRAINT `randevu_ibfk_2` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `renkler`
--

DROP TABLE IF EXISTS `renkler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `renkler` (
  `HayvanID` int NOT NULL,
  `Renk` varchar(100) NOT NULL,
  PRIMARY KEY (`HayvanID`,`Renk`),
  CONSTRAINT `renkler_ibfk_1` FOREIGN KEY (`HayvanID`) REFERENCES `hastahayvan` (`HastaID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reviewverir`
--

DROP TABLE IF EXISTS `reviewverir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviewverir` (
  `HayvanSahibiID` int NOT NULL,
  `VeterinerID` int NOT NULL,
  `Açıklama` varchar(255) DEFAULT NULL,
  `Puan` int NOT NULL,
  PRIMARY KEY (`HayvanSahibiID`,`VeterinerID`),
  KEY `VeterinerID` (`VeterinerID`),
  CONSTRAINT `reviewverir_ibfk_1` FOREIGN KEY (`HayvanSahibiID`) REFERENCES `hayvansahibi` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reviewverir_ibfk_2` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `reçete`
--

DROP TABLE IF EXISTS `reçete`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reçete` (
  `ReçeteID` int NOT NULL AUTO_INCREMENT,
  `Tarih` datetime DEFAULT NULL,
  `VeterinerID` int NOT NULL,
  `HastaHayvanID` int NOT NULL,
  PRIMARY KEY (`ReçeteID`),
  KEY `VeterinerID` (`VeterinerID`),
  KEY `HastaHayvanID` (`HastaHayvanID`),
  CONSTRAINT `reçete_ibfk_1` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reçete_ibfk_2` FOREIGN KEY (`HastaHayvanID`) REFERENCES `hastahayvan` (`HastaID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `saatler`
--

DROP TABLE IF EXISTS `saatler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saatler` (
  `SaatID` int NOT NULL AUTO_INCREMENT,
  `Gün` enum('Pazartesi','Salı','Çarşamba','Perşembe','Cuma') NOT NULL,
  `Saat` int NOT NULL,
  `Dakika` int NOT NULL,
  PRIMARY KEY (`SaatID`),
  CONSTRAINT `saatler_chk_1` CHECK ((`Saat` < 24)),
  CONSTRAINT `saatler_chk_2` CHECK ((`Dakika` < 60))
) ENGINE=InnoDB AUTO_INCREMENT=241 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `uygundur`
--

DROP TABLE IF EXISTS `uygundur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uygundur` (
  `SaatID` int NOT NULL,
  `VeterinerID` int NOT NULL,
  PRIMARY KEY (`SaatID`,`VeterinerID`),
  KEY `VeterinerID` (`VeterinerID`),
  CONSTRAINT `uygundur_ibfk_1` FOREIGN KEY (`SaatID`) REFERENCES `saatler` (`SaatID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `uygundur_ibfk_2` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `veteriner`
--

DROP TABLE IF EXISTS `veteriner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `veteriner` (
  `KullanıcıID` int NOT NULL,
  `İsim` varchar(255) NOT NULL,
  `Soyisim` varchar(255) NOT NULL,
  `TCNO` varchar(11) NOT NULL,
  `TelefonNo` varchar(11) DEFAULT NULL,
  `İlçe` varchar(255) DEFAULT NULL,
  `Mahalle` varchar(255) DEFAULT NULL,
  `İl` varchar(255) DEFAULT NULL,
  `OdaNO` int DEFAULT NULL,
  `AdminID` int NOT NULL,
  PRIMARY KEY (`KullanıcıID`),
  UNIQUE KEY `TCNO` (`TCNO`),
  KEY `AdminID` (`AdminID`),
  CONSTRAINT `veteriner_ibfk_1` FOREIGN KEY (`KullanıcıID`) REFERENCES `kullanıcı` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `veteriner_ibfk_2` FOREIGN KEY (`AdminID`) REFERENCES `admin` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `chk_TCNO_length` CHECK ((char_length(`TCNO`) = 11)),
  CONSTRAINT `chk_TelefonNo_length` CHECK (((`TelefonNo` is null) or (char_length(`TelefonNo`) = 11)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `yetkinlik`
--

DROP TABLE IF EXISTS `yetkinlik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yetkinlik` (
  `VeterinerID` int NOT NULL,
  `Yetkinlik` enum('Kedi','Köpek','Kuş','Tavşan','Kaplumbağa','Hamster','Kobay') NOT NULL,
  PRIMARY KEY (`VeterinerID`,`Yetkinlik`),
  CONSTRAINT `temp` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-23 22:27:24
