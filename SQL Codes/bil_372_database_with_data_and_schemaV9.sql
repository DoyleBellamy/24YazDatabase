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
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1),(2),(3),(4),(5);
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `hastahayvan`
--

LOCK TABLES `hastahayvan` WRITE;
/*!40000 ALTER TABLE `hastahayvan` DISABLE KEYS */;
INSERT INTO `hastahayvan` VALUES (81,21,18,44,'Jeromy',9.2,'Kedi','Erkek'),(82,22,16,100,'Felicia',5.4,'Kuş','Erkek'),(83,23,9,13,'Dustin',3,'Tavşan','Erkek'),(84,24,7,15,'Dawson',7.6,'Tavşan','Erkek'),(85,25,4,48,'Junior',3.4,'Tavşan','Erkek'),(86,26,19,68,'May',8.2,'Kedi','Erkek'),(87,27,20,30,'Blanca',9.7,'Kedi','Erkek'),(88,28,1,34,'Katelynn',7.3,'Kedi','Erkek'),(89,29,17,24,'Cloyd',1.4,'Köpek','Erkek'),(90,30,11,21,'Leslie',2.7,'Köpek','Dişi'),(91,31,18,19,'Levi',4.5,'Kedi','Dişi'),(92,32,4,85,'Madison',1.9,'Köpek','Erkek'),(93,33,7,64,'Celestine',6.8,'Hamster','Dişi'),(94,34,22,36,'Javon',8,'Hamster','Erkek'),(95,35,25,73,'Tre',2.5,'Kuş','Dişi'),(96,36,13,67,'Sanford',1.8,'Hamster','Erkek'),(97,37,18,61,'Joyce',4.9,'Kedi','Erkek'),(98,38,20,52,'Noelia',8.8,'Kedi','Erkek'),(99,39,24,70,'Patience',3.8,'Kuş','Erkek'),(100,40,5,70,'Otho',7.7,'Hamster','Dişi'),(101,41,23,27,'Adelia',4.3,'Hamster','Erkek'),(102,42,10,24,'Brielle',5.9,'Hamster','Dişi'),(103,43,19,80,'Judah',4.3,'Hamster','Dişi'),(104,44,4,29,'Cecilia',3.5,'Hamster','Erkek'),(105,45,15,22,'Eduardo',8,'Kaplumbağa','Dişi'),(106,46,23,69,'Wallace',1.5,'Kedi','Dişi'),(107,47,23,68,'Gerda',7.7,'Kedi','Dişi'),(108,48,16,74,'Luella',9.1,'Hamster','Erkek'),(109,49,2,88,'Drake',6.6,'Hamster','Erkek'),(110,50,19,31,'Reece',6.3,'Köpek','Erkek'),(111,51,16,10,'Zelda',0.6,'Hamster','Dişi'),(112,52,14,90,'Filiberto',7.5,'Kuş','Dişi'),(113,53,1,80,'Gonzalo',0.2,'Kedi','Dişi'),(114,54,22,67,'Urban',8,'Köpek','Erkek'),(115,55,17,12,'Mossie',5.3,'Kaplumbağa','Dişi'),(116,56,14,95,'Kelley',1.6,'Kuş','Erkek'),(117,57,21,90,'Edgardo',7,'Kedi','Erkek'),(118,58,19,80,'Joel',7.9,'Hamster','Dişi'),(119,59,13,43,'Jeremy',7.5,'Kaplumbağa','Erkek'),(120,60,17,18,'Ahmad',8.1,'Köpek','Dişi'),(121,61,5,43,'Candido',9,'Tavşan','Erkek'),(122,62,16,15,'Jensen',9.1,'Hamster','Erkek'),(123,63,12,44,'Julian',7,'Kuş','Erkek'),(124,64,24,83,'Carlo',9.9,'Hamster','Erkek'),(125,65,12,46,'Theresia',3.5,'Kuş','Dişi'),(126,66,19,100,'Britney',2.1,'Tavşan','Dişi'),(127,67,18,12,'Paul',0.7,'Hamster','Erkek'),(128,68,11,55,'Nat',8,'Köpek','Dişi'),(129,69,3,59,'Nikita',3.5,'Hamster','Erkek'),(130,70,25,59,'Laura',1.9,'Hamster','Dişi'),(131,71,18,22,'Antonia',2.4,'Kaplumbağa','Erkek'),(132,72,3,21,'Willie',7.4,'Hamster','Erkek'),(133,73,8,79,'Letha',2.2,'Tavşan','Dişi'),(134,74,12,54,'Luna',1.5,'Kuş','Erkek'),(135,75,20,11,'Arch',1.6,'Kaplumbağa','Dişi'),(136,76,10,14,'Sarina',3.8,'Hamster','Erkek'),(137,77,17,34,'Henri',0.8,'Köpek','Erkek'),(138,78,12,84,'Akeem',8.3,'Hamster','Erkek'),(139,79,3,98,'Deangelo',3,'Kuş','Erkek'),(140,80,14,24,'Berenice',8.5,'Kedi','Dişi'),(141,81,17,42,'Twila',3.9,'Tavşan','Erkek'),(142,82,3,16,'Merle',7.7,'Kedi','Dişi'),(143,83,8,92,'Augustine',4,'Hamster','Dişi'),(144,84,14,63,'Jeromy',7.2,'Tavşan','Dişi'),(145,85,14,19,'Hilbert',8.4,'Kaplumbağa','Dişi'),(146,86,17,69,'Georgette',5.8,'Hamster','Dişi'),(147,87,9,25,'Eileen',0.6,'Tavşan','Dişi'),(148,88,18,22,'Carley',7,'Kedi','Erkek'),(149,89,11,98,'Antonina',0.5,'Hamster','Erkek'),(150,90,15,57,'Howell',2.2,'Kuş','Erkek'),(151,91,5,22,'Lupe',4.1,'Hamster','Dişi'),(152,92,3,48,'Abelardo',6.3,'Kuş','Erkek'),(153,93,3,32,'Shania',7.8,'Köpek','Erkek'),(154,94,16,73,'Edgardo',6.2,'Hamster','Erkek'),(155,95,9,20,'Marcelino',3.9,'Kuş','Erkek'),(156,96,21,49,'Sydnee',0.5,'Kedi','Dişi'),(157,97,18,48,'Zita',2.9,'Kaplumbağa','Erkek'),(158,98,21,56,'Aaron',1.5,'Köpek','Dişi'),(159,99,21,10,'Stephany',2,'Köpek','Erkek'),(160,100,6,18,'Jordan',3.1,'Köpek','Dişi');
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
  CONSTRAINT `hayvansahibi_ibfk_1` FOREIGN KEY (`KullanıcıID`) REFERENCES `kullanıcı` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hayvansahibi`
--

LOCK TABLES `hayvansahibi` WRITE;
/*!40000 ALTER TABLE `hayvansahibi` DISABLE KEYS */;
INSERT INTO `hayvansahibi` VALUES (21,'Marcia','Langosh','Arkansas','Avon','Grand Prairie'),(22,'Elmo','Gerhold','Montana','Avon','San Buenaventura (Ventura)'),(23,'Geovanny','Osinski','Oregon','Borders','Jeffersonville'),(24,'Effie','Paucek','Nevada','Buckinghamshire','Ann Arbor'),(25,'Lourdes','Mueller','Oklahoma','Berkshire','Inglewood'),(26,'Sheridan','Lubowitz','Florida','Buckinghamshire','Hemet'),(27,'Leone','Moore','Alabama','Borders','Woodland'),(28,'Grayson','Hodkiewicz','Maryland','Bedfordshire','Champaign'),(29,'Louie','Glover','Nebraska','Avon','Bayamon'),(30,'Lilly','Boehm','Oklahoma','Cambridgeshire','Tustin'),(31,'Lesly','Krajcik','Arkansas','Berkshire','Lake Elsinore'),(32,'Cleta','King','Montana','Avon','St. Petersburg'),(33,'Onie','Pfannerstill','North Carolina','Avon','Aloha'),(34,'Kody','Daugherty','Kansas','Bedfordshire','Murrieta'),(35,'Lexie','Satterfield','Wyoming','Cambridgeshire','Oro Valley'),(36,'Jamar','Hahn','New York','Bedfordshire','Canton'),(37,'Jamir','Kuhlman','Washington','Avon','Stamford'),(38,'Kaitlyn','Prohaska','West Virginia','Cambridgeshire','Draper'),(39,'Shanie','Zboncak','Colorado','Avon','Southfield'),(40,'Torrey','Jaskolski','Oklahoma','Berkshire','Palm Coast'),(41,'Emmett','Steuber','Pennsylvania','Berkshire','Rialto'),(42,'Justine','Borer','New Jersey','Bedfordshire','Longmont'),(43,'Jerod','Deckow','Connecticut','Buckinghamshire','Tacoma'),(44,'Eleanora','Labadie','Louisiana','Buckinghamshire','Lehi'),(45,'Agustin','Aufderhar','South Dakota','Borders','Riverton'),(46,'Aurelio','Paucek','North Carolina','Cambridgeshire','Waterbury'),(47,'Ezekiel','Douglas','Oregon','Borders','Clearwater'),(48,'Adrien','Prosacco','Louisiana','Bedfordshire','Indianapolis'),(49,'Janessa','Greenholt','Arizona','Avon','Kendale Lakes'),(50,'Meta','Ryan','Kansas','Cambridgeshire','Henderson'),(51,'Stanford','Reilly','Washington','Borders','Greenville'),(52,'Florida','Macejkovic','Tennessee','Bedfordshire','Corpus Christi'),(53,'Lilliana','Bernhard','Idaho','Borders','Bowling Green'),(54,'Fausto','Towne','Arkansas','Cambridgeshire','Decatur'),(55,'Alf','Brown','Georgia','Borders','St. Paul'),(56,'Roselyn','Glover','Nevada','Berkshire','North Las Vegas'),(57,'Alexandrea','Metz','Kansas','Berkshire','Brookline'),(58,'Aiden','Weber','Oklahoma','Borders','Casa Grande'),(59,'Kristy','Volkman','Iowa','Berkshire','Billings'),(60,'Alivia','Kunze','Connecticut','Cambridgeshire','Chula Vista'),(61,'Stella','Wolf','South Dakota','Buckinghamshire','Mesa'),(62,'Bobby','Amore','Florida','Buckinghamshire','Buena Park'),(63,'Jan','Powlowski','South Dakota','Avon','Dale City'),(64,'Nestor','Schinner','California','Cambridgeshire','Dublin'),(65,'Krystal','Amore','Illinois','Bedfordshire','East Orange'),(66,'Alfonzo','Schumm','Texas','Buckinghamshire','Salt Lake City'),(67,'Brock','Hane','New York','Buckinghamshire','St. Joseph'),(68,'Adah','Spencer','Kentucky','Buckinghamshire','Conway'),(69,'Scot','Bednar','Minnesota','Buckinghamshire','Framingham'),(70,'Camille','Bahringer','New Hampshire','Avon','Bowling Green'),(71,'Ericka','Ryan','Maryland','Buckinghamshire','Salinas'),(72,'Reanna','Marquardt','Arkansas','Bedfordshire','Caldwell'),(73,'Adaline','Greenfelder','Nevada','Avon','Bozeman'),(74,'Pearlie','Rosenbaum','North Carolina','Buckinghamshire','Fremont'),(75,'Adeline','Dach','Wyoming','Cambridgeshire','Oakland'),(76,'Henri','Farrell','South Dakota','Avon','West Sacramento'),(77,'Ted','Schowalter','Missouri','Berkshire','Tulsa'),(78,'Emily','Jones','South Dakota','Berkshire','Upland'),(79,'Molly','Lowe','Connecticut','Bedfordshire','University'),(80,'Jaleel','Walker','Alaska','Berkshire','Kissimmee'),(81,'Brennon','Keefe','Delaware','Bedfordshire','Port Orange'),(82,'Jason','Huels','Arizona','Bedfordshire','Dothan'),(83,'Garnett','Swaniawski','Wyoming','Borders','St. Louis Park'),(84,'Taya','Pfeffer','Iowa','Berkshire','Sunrise'),(85,'Halie','Effertz','Vermont','Borders','Caldwell'),(86,'Nathen','Wisozk','Michigan','Buckinghamshire','Irondequoit'),(87,'Chasity','Price','North Carolina','Buckinghamshire','San Buenaventura (Ventura)'),(88,'Yvonne','Boyer','North Carolina','Bedfordshire','Carlsbad'),(89,'Lenny','Mann','Wyoming','Borders','Cedar Park'),(90,'Cyrus','Franecki','Kentucky','Borders','Carolina'),(91,'Akeem','Brown','Nebraska','Bedfordshire','Melbourne'),(92,'Anabelle','Gleichner','Montana','Buckinghamshire','Gainesville'),(93,'Alessandra','Fisher','Nebraska','Berkshire','Fort Lauderdale'),(94,'Ericka','Dickinson','Minnesota','Berkshire','Maricopa'),(95,'Marty','Rippin','Indiana','Buckinghamshire','Denver'),(96,'Jermaine','Ortiz','South Dakota','Bedfordshire','Nashua'),(97,'Shania','Dooley','Nevada','Buckinghamshire','San Bernardino'),(98,'Gerard','Boyle','Minnesota','Buckinghamshire','Kansas City'),(99,'Libby','Towne','Alabama','Avon','Vancouver'),(100,'Jarred','Yundt','Alaska','Berkshire','Folsom');
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
-- Dumping data for table `ilaçlar`
--

LOCK TABLES `ilaçlar` WRITE;
/*!40000 ALTER TABLE `ilaçlar` DISABLE KEYS */;
INSERT INTO `ilaçlar` VALUES (3,'Bettie','38040.9','4082',5),(4,'Marlon','31531.5','1131',3),(5,'Ebba','45922.5','3167',1),(6,'Opal','42609','1126',4),(7,'Layne','526.5','3506',4),(8,'Candido','42983.1','2439',1),(9,'Margarita','32353.8','4906',1),(10,'Crawford','29676.899999999998','3746',5),(11,'Davin','8782.8','2955',1),(12,'Aric','45059.1','1754',1),(13,'Jodie','15630','3986',5),(14,'Deja','19518.3','4853',1),(15,'Kailee','13297.5','1474',4),(16,'Charles','45140.7','4325',1),(17,'Felix','23169.899999999998','4311',5),(18,'Grover','30708.899999999998','3531',4),(19,'Shea','41175','4820',3),(20,'Jacques','24569.399999999998','2885',5),(21,'Omari','43242.9','3933',5),(22,'Brody','30846.899999999998','3405',3),(23,'Monte','15732.599999999999','1278',3),(24,'Dawson','8404.5','2367',3),(25,'Lelah','37369.2','3427',5),(26,'Hugh','33362.4','3021',1),(27,'Ubaldo','14238','3397',2),(28,'Regan','33430.799999999996','3377',4),(29,'Kyra','47474.7','2874',5),(30,'Estrella','20759.1','1124',4),(31,'Hilma','4049.7','3064',4),(32,'Brooke','36564.9','2915',5),(33,'Eunice','40835.4','2921',2),(34,'Cody','38704.2','3196',1),(35,'Trent','5622','2215',1),(36,'Emmalee','32434.199999999997','4082',1),(37,'Astrid','25639.5','2129',2),(38,'Leila','8521.8','1053',5),(39,'Dallin','27240.3','3286',5),(40,'Brandon','32599.199999999997','4035',2),(41,'Izabella','23923.8','4110',2),(42,'Tara','43839.6','1308',2),(43,'Mekhi','37926.6','4115',2),(44,'Howell','39064.2','1529',3),(45,'John','11569.8','3333',3),(46,'Keenan','7418.7','4278',2),(47,'Elissa','43389.6','4326',2),(48,'Cassidy','34496.4','3309',1),(49,'Anna','45663.9','4527',2),(50,'Anastasia','41300.7','3613',1),(51,'Rubie','35743.5','2988',1),(52,'Celia','15752.4','2799',1),(53,'Dena','4904.4','4813',5),(54,'Jaylon','42373.799999999996','1782',5),(55,'Georgette','2802.2999999999997','4604',5),(56,'Elna','8761.199999999999','1061',1),(57,'Alfred','43122.299999999996','1442',2),(58,'Odie','14133','1375',2),(59,'Wiley','17809.8','2408',1),(60,'Faustino','24986.1','3121',3),(61,'Gage','6831.599999999999','1985',5),(62,'Geoffrey','12000','4644',1),(63,'Zander','45042','4927',1),(64,'Sid','6092.4','3353',1),(65,'Denis','44744.4','1294',3),(66,'Vivian','25058.399999999998','3465',5),(67,'Chance','39834','3356',2),(68,'Leif','14429.099999999999','1719',1),(69,'Otis','29159.699999999997','3103',3),(70,'Deja','13726.5','3703',2),(71,'Isadore','36470.1','4812',4),(72,'Erwin','44402.4','2919',1),(73,'Daren','14946.599999999999','3326',1),(74,'Lacy','2247.6','1032',5),(75,'Durward','2285.1','3147',5),(76,'Sigurd','29970.6','1694',5),(77,'Micah','13741.5','2501',1),(78,'Jalyn','17961','3206',5),(79,'Aditya','3909.6','2057',2),(80,'Hugh','29543.399999999998','2594',2),(81,'Arnoldo','15081.3','3391',4),(82,'Athena','16293.599999999999','3244',4),(83,'Astrid','37329.299999999996','2099',1),(84,'Wilson','21487.8','4916',1),(85,'Felipe','25464','2333',4),(86,'Mellie','45865.2','1873',5),(87,'Lizzie','10653','2770',3),(88,'Greta','2662.2','4854',4),(89,'Isac','46920.299999999996','2367',5),(90,'Jade','13672.199999999999','4187',5),(91,'Annette','7675.799999999999','1754',5),(92,'Sadie','20430.3','4006',5),(93,'Elvie','9020.1','3302',2),(94,'Jordy','14356.8','2524',2),(95,'Ahmed','3244.5','3999',3),(96,'Jermey','49642.2','1339',3),(97,'Cornell','11051.4','4858',5),(98,'Odessa','39494.7','4405',1),(99,'Justen','28065.3','2504',2),(100,'Oda','3936.6','4693',2),(101,'Esperanza','26679.6','4631',2),(102,'Clint','19356.3','1744',5);
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
  CONSTRAINT `içerir_ibfk_1` FOREIGN KEY (`İlaçID`) REFERENCES `ilaçlar` (`İlaçID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `içerir_ibfk_2` FOREIGN KEY (`ReçeteID`) REFERENCES `reçete` (`ReçeteID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `içerir`
--

LOCK TABLES `içerir` WRITE;
/*!40000 ALTER TABLE `içerir` DISABLE KEYS */;
INSERT INTO `içerir` VALUES (41,1),(62,1),(82,1),(93,2),(43,4),(90,4),(51,5),(27,6),(85,6),(6,7),(26,7),(85,9),(39,10),(29,11),(19,12),(38,12),(94,12),(32,13),(35,14),(24,16),(31,17),(36,17),(63,17),(35,19),(44,19),(2,20),(31,21),(52,22),(77,24),(72,25),(82,25),(96,25),(55,26),(65,27),(45,28),(6,30),(93,31),(90,33),(25,34),(55,34),(64,34),(72,35),(57,38),(98,39),(3,40),(67,40),(84,42),(0,43),(9,46),(63,47),(76,47),(0,48),(22,48),(21,50),(33,51),(74,51),(43,53),(47,53),(50,53),(78,57),(2,58),(20,58),(97,58),(79,59),(75,61),(99,61),(62,65),(90,66),(23,70),(76,70),(64,72),(7,73),(80,73),(36,76),(53,78),(32,79),(46,79),(71,81),(7,83),(83,83),(13,84),(64,85),(27,87),(3,88),(34,89),(72,89),(87,89),(92,89),(8,91),(29,91),(68,91),(41,92),(40,94),(61,94),(71,94),(42,97),(8,98),(12,98),(31,98),(86,100);
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
  PRIMARY KEY (`KullanıcıID`),
  UNIQUE KEY `Email` (`Email`),
  CONSTRAINT `kullanıcı_chk_1` CHECK (((`Rol` = _utf8mb3'admin') or (`Rol` = _utf8mb3'veteriner') or (`Rol` = _utf8mb3'kullanıcı')))
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kullanıcı`
--

LOCK TABLES `kullanıcı` WRITE;
/*!40000 ALTER TABLE `kullanıcı` DISABLE KEYS */;
INSERT INTO `kullanıcı` VALUES (1,'a','1','admin'),(2,'Janiya_Marvin@gmail.com','Yd3Q_V39nhl5a4G','admin'),(3,'Josue.Shields@gmail.com','b78uNvGHS6aeKql','admin'),(4,'Maybell_Wisoky@hotmail.com','_zryqtj44PFZys0','admin'),(5,'Alfonzo_Stracke53@hotmail.com','95VnZqmFt30NO2e','admin'),(6,'b','2','veteriner'),(7,'Peyton_Hilpert98@hotmail.com','Pz_T3PSnxA8RyBk','veteriner'),(8,'Willard69@hotmail.com','rHXrheNrG8TfUP4','veteriner'),(9,'Evangeline33@gmail.com','GY63t9b51_39xF2','veteriner'),(10,'Henry.Abshire98@yahoo.com','SGmcdZunQNI6764','veteriner'),(11,'Ismael_Trantow51@gmail.com','xeVW6hdYDlkLTyJ','veteriner'),(12,'Triston.Baumbach8@hotmail.com','X_HGwB6HPUU8zWB','veteriner'),(13,'Arturo.Runolfsson35@yahoo.com','jqA3qOkXEtJaIHE','veteriner'),(14,'Kaela_Reynolds@hotmail.com','lo6saCLaKDEDLUj','veteriner'),(15,'Don_Luettgen98@yahoo.com','lllKzuL18LB7Zcb','veteriner'),(16,'Miguel60@gmail.com','dVEFrPxVW0kDn9s','veteriner'),(17,'Faye93@gmail.com','0mn0eaLGQGO0nNW','veteriner'),(18,'Melyna44@hotmail.com','GT475ExbjQLTCrO','veteriner'),(19,'Emilie98@yahoo.com','YqncvXlr1Dqo6LS','veteriner'),(20,'Terrill_Bergstrom@gmail.com','6LoV5ZDmqLiQHOj','veteriner'),(21,'c','3','kullanıcı'),(22,'Michale.Bednar10@hotmail.com','H52XsUKem6byktl','kullanıcı'),(23,'Taryn.Fahey@hotmail.com','6o_tMFviLTQMmim','kullanıcı'),(24,'Dustin96@gmail.com','3MJHRKq5NweFQ2g','kullanıcı'),(25,'Natasha.Huels18@gmail.com','2MtgUMpsYFrSOpT','kullanıcı'),(26,'Matilde_Prohaska@hotmail.com','RbFrTnaMGv_zMyf','kullanıcı'),(27,'Mackenzie59@yahoo.com','BGZgtJs9xNDhO4U','kullanıcı'),(28,'Renee.Ortiz@yahoo.com','zJTxFp66FgzIA8D','kullanıcı'),(29,'Eriberto.Purdy@yahoo.com','RPOzQR2ixooO9ec','kullanıcı'),(30,'Makenna_Hills11@gmail.com','5l7Xc2LVoGxAuWE','kullanıcı'),(31,'Suzanne.Cummerata85@gmail.com','kGHwtnwomtjNmd8','kullanıcı'),(32,'Joesph16@gmail.com','_sgbhGHN_EMMS52','kullanıcı'),(33,'Ladarius14@yahoo.com','1d_uREssMfmDm5I','kullanıcı'),(34,'Major54@yahoo.com','PAeSt__c_Qe01VJ','kullanıcı'),(35,'Asa15@gmail.com','Iq2qpaCC8R2DQaK','kullanıcı'),(36,'Ransom34@gmail.com','goWLi8kJXwL4UMh','kullanıcı'),(37,'Mac.Mraz50@gmail.com','aUYDrxRb5j7ttJz','kullanıcı'),(38,'Jaunita.Feeney@gmail.com','81TW94ZYh7kUZqN','kullanıcı'),(39,'Susie.Nitzsche76@hotmail.com','MNuNuxXnLUvZvcJ','kullanıcı'),(40,'Erika50@yahoo.com','vVjVPrk6JYav6XL','kullanıcı'),(41,'Opal_Medhurst24@yahoo.com','zb9QI6bvf3AOORe','kullanıcı'),(42,'Johnpaul.Wilkinson@yahoo.com','qeotmUY8Wws06Qi','kullanıcı'),(43,'Kelsi27@yahoo.com','NszogXfinmLS9_3','kullanıcı'),(44,'Rory.Klocko3@hotmail.com','xqb08q4wejLQ1QF','kullanıcı'),(45,'Mariela40@hotmail.com','3qClV7EOcTFdazf','kullanıcı'),(46,'Jailyn.Kreiger65@gmail.com','fMDPPnAwxAfqSp7','kullanıcı'),(47,'Grant44@gmail.com','I6oqqJj33xcaLgh','kullanıcı'),(48,'Fiona.Emard7@yahoo.com','hGciODesUqS3Ogt','kullanıcı'),(49,'Payton_OConnell@hotmail.com','e4HAz7Cjuj87ULo','kullanıcı'),(50,'Silas.McCullough@yahoo.com','eBf6pD1zig1MS8Q','kullanıcı'),(51,'Lela_Hudson@yahoo.com','t1YKxdCXjSqi6MU','kullanıcı'),(52,'Asa_Blick@hotmail.com','jUgtgtvtyBze8R4','kullanıcı'),(53,'Frederick_Hilpert40@gmail.com','5PXHikhGUM2AarT','kullanıcı'),(54,'Oliver.Barrows71@hotmail.com','ocDyEmrsWvUdKv_','kullanıcı'),(55,'Kamren.Rutherford@yahoo.com','diU67HY207qKb9l','kullanıcı'),(56,'Cheyanne2@yahoo.com','IZaj5kUV8mL_Snd','kullanıcı'),(57,'Donnell_Stark99@gmail.com','8puHpJ0uFI94YyB','kullanıcı'),(58,'Chandler60@gmail.com','XVhgjWWFF6cNhvC','kullanıcı'),(59,'Lilian_Howell32@gmail.com','BzN1hJ4DSI1VHvQ','kullanıcı'),(60,'Liana_Carroll21@yahoo.com','SkGfjwBvK7o3ebj','kullanıcı'),(61,'Jedidiah.Kulas@yahoo.com','bRwSqrURRErqT3u','kullanıcı'),(62,'Burley.MacGyver@yahoo.com','pdj56XaU8Nu4qVe','kullanıcı'),(63,'Sierra_Jaskolski@yahoo.com','2DVvA5RvvQg3Str','kullanıcı'),(64,'Ayla96@yahoo.com','EDZAMBsIQyW0Cwb','kullanıcı'),(65,'Valentina.Wunsch@yahoo.com','_6Dnbi48NZJTDeA','kullanıcı'),(66,'Kris.Bednar@hotmail.com','EjGZJ00YVGnF44L','kullanıcı'),(67,'Haylee_Keeling22@gmail.com','ZhFbMBUbo0mnp_6','kullanıcı'),(68,'Cristal34@yahoo.com','XuGfxlaJOQ9lsM8','kullanıcı'),(69,'Zion_Abshire19@gmail.com','vblwBgv6iPTY0WY','kullanıcı'),(70,'Abel.Gibson2@hotmail.com','95NiX16htfJIr51','kullanıcı'),(71,'Adeline41@yahoo.com','5AuHc6_AMkEDtB0','kullanıcı'),(72,'Evert77@yahoo.com','3Mp29ptdH9UXILu','kullanıcı'),(73,'Forrest.Cronin@yahoo.com','l_IT6fWOP4b0wE7','kullanıcı'),(74,'Marge55@gmail.com','YaKWg1To4189Ykc','kullanıcı'),(75,'Jeff.Von12@yahoo.com','pKFiLF6g6DJYjWf','kullanıcı'),(76,'Alexander_Boyle@hotmail.com','BFMqlRmG6DCC3Ju','kullanıcı'),(77,'Matt_Pacocha92@yahoo.com','JVdRl068gmBSevV','kullanıcı'),(78,'Isobel.Gleason@yahoo.com','Ye4AzO1vK2zV5kt','kullanıcı'),(79,'Krystal.Volkman97@yahoo.com','In7ANMheNMD0UTA','kullanıcı'),(80,'Rowan.Franecki44@gmail.com','Wpy8beLP856LDdg','kullanıcı'),(81,'Dusty13@gmail.com','NuUEuT7ovUvmvkN','kullanıcı'),(82,'Christophe_Swift@yahoo.com','PVQ0GHqQmkCWlmW','kullanıcı'),(83,'Dax35@gmail.com','ode1LFblh97Cwa7','kullanıcı'),(84,'Albin.Herzog@hotmail.com','I_W_Sa__Zfx4Nmb','kullanıcı'),(85,'Kenna.Hettinger@hotmail.com','FlNNQIBjR3iJTu9','kullanıcı'),(86,'Hulda44@yahoo.com','BlYEVF_2GonTxJH','kullanıcı'),(87,'Ashley.Fadel@hotmail.com','DsKxvC1KfW5rXxu','kullanıcı'),(88,'Barbara78@yahoo.com','6Rs6VY052OhJCoM','kullanıcı'),(89,'Lilliana.Batz24@hotmail.com','QiDQw_KdSB3bBVc','kullanıcı'),(90,'Nathanial95@yahoo.com','RhE1t5LkfGWqYxO','kullanıcı'),(91,'Barry_Cummings@gmail.com','S49gypejVk4JaOG','kullanıcı'),(92,'Patsy.Kirlin3@hotmail.com','6w_9omV19Q92Ov3','kullanıcı'),(93,'Parker62@yahoo.com','Bmp0FLuo6kSFKng','kullanıcı'),(94,'Reta.Ebert@gmail.com','nm5L0oqtHdwskxk','kullanıcı'),(95,'Hoyt_Dicki46@gmail.com','LrYnj18MJ0nS2XV','kullanıcı'),(96,'Nolan80@yahoo.com','X69G4VTLksHFA0z','kullanıcı'),(97,'Loma62@yahoo.com','uT1FY1VDnolGKYq','kullanıcı'),(98,'Antonietta_Hamill78@gmail.com','59QTpYyZCmsALv4','kullanıcı'),(99,'Spencer24@hotmail.com','5AhqG0nww_FIcz9','kullanıcı'),(100,'Maiya_Waters@hotmail.com','MbLd0ZSrZyQ5x4E','kullanıcı');
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
  CONSTRAINT `muayenefaturası_ibfk_1` FOREIGN KEY (`SahipID`) REFERENCES `hayvansahibi` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=153 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `muayenefaturası`
--

LOCK TABLES `muayenefaturası` WRITE;
/*!40000 ALTER TABLE `muayenefaturası` DISABLE KEYS */;
INSERT INTO `muayenefaturası` VALUES (3,74,2305.5),(4,74,1088),(5,69,1110),(6,28,1901.5),(7,42,993.5),(8,37,422),(9,48,2061.5),(10,54,734),(11,21,1075.5),(12,98,4085.5),(13,35,2579),(14,36,4134),(15,58,2043.5),(16,26,788.5),(17,74,341.5),(18,76,3858),(19,41,4257),(20,35,4455),(21,98,703.5),(22,29,3196),(23,97,583.5),(24,21,1936.5),(25,84,3758),(26,49,3309.5),(27,36,4643.5),(28,49,1650.5),(29,38,2336),(30,83,1853),(31,27,2458),(32,23,3789),(33,87,4274.5),(34,42,2432),(35,64,2357),(36,99,4298),(37,96,1133),(38,37,4084.5),(39,84,4518.5),(40,45,2005),(41,63,3706.5),(42,62,4736.5),(43,59,1782),(44,40,3943),(45,93,853.5),(46,41,2381),(47,55,502),(48,37,3867),(49,71,1164.5),(50,79,3732.5),(51,45,1811.5),(52,92,4640.5),(53,21,937),(54,92,2481),(55,90,4911.5),(56,49,632),(57,58,1084),(58,52,4221.5),(59,83,609),(60,33,1856),(61,57,4954),(62,55,4180),(63,69,2076.5),(64,83,1757),(65,30,835.5),(66,98,4683),(67,66,4739),(68,44,1431.5),(69,59,4163.5),(70,60,1838.5),(71,22,463),(72,79,1672),(73,59,1167.5),(74,62,3176.5),(75,47,477),(76,92,1994.5),(77,35,4756),(78,24,509),(79,91,2843.5),(80,71,1068.5),(81,54,2042.5),(82,90,2191),(83,72,3908),(84,54,3539.5),(85,64,3808),(86,86,2768),(87,58,2062.5),(88,53,1456),(89,39,664.5),(90,38,2332),(91,85,2076),(92,50,3658),(93,77,946),(94,55,3914.5),(95,42,3315),(96,28,3929.5),(97,29,1798),(98,92,2583.5),(99,43,1027.5),(100,30,1631.5),(101,87,4707.5),(102,64,1785.5),(103,55,3569.5),(104,95,3102.5),(105,64,2826.5),(106,93,3664),(107,74,4479),(108,46,1484),(109,21,1813.5),(110,97,3391.5),(111,59,4102),(112,91,4403),(113,59,1661),(114,50,566.5),(115,77,1746),(116,39,1318),(117,24,2229),(118,49,3940),(119,25,4817),(120,41,2212),(121,98,2226),(122,54,4045),(123,51,3383),(124,99,1217),(125,95,963),(126,26,2314.5),(127,71,647.5),(128,66,2533),(129,89,4172),(130,94,3731.5),(131,71,1655.5),(132,82,3729.5),(133,84,4871.5),(134,48,1754.5),(135,55,749),(136,74,603),(137,99,1698),(138,41,4535.5),(139,82,4754),(140,53,4346.5),(141,96,3251),(142,59,557.5),(143,75,2538.5),(144,42,4008),(145,88,4606.5),(146,97,413),(147,26,1062.5),(148,32,745.5),(149,60,2994.5),(150,97,3806),(151,87,799.5),(152,95,4953.5);
/*!40000 ALTER TABLE `muayenefaturası` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `randevu`
--

LOCK TABLES `randevu` WRITE;
/*!40000 ALTER TABLE `randevu` DISABLE KEYS */;
INSERT INTO `randevu` VALUES (13,21,'2023-08-14 14:51:29'),(16,22,'2023-12-17 14:51:29'),(20,23,'2024-05-18 09:31:29'),(9,24,'2024-10-04 06:51:29'),(11,24,'2023-08-28 12:11:29'),(15,27,'2024-06-29 01:31:29'),(20,27,'2024-09-20 09:31:29'),(20,33,'2024-10-18 04:11:29'),(7,35,'2024-07-26 20:11:29'),(15,35,'2023-11-05 22:51:29'),(14,41,'2024-01-28 06:51:29'),(6,47,'2024-02-25 01:31:29'),(16,48,'2023-12-03 17:31:29'),(10,49,'2023-10-23 01:31:29'),(18,49,'2024-05-04 12:11:29'),(16,52,'2024-02-11 04:11:29'),(11,56,'2023-10-09 04:11:29'),(9,58,'2024-06-01 06:51:29'),(9,59,'2024-04-20 14:51:29'),(15,60,'2023-07-31 17:31:29'),(18,61,'2024-09-06 12:11:29'),(17,64,'2024-11-14 22:51:29'),(9,65,'2024-03-23 20:11:29'),(16,65,'2024-11-01 01:31:29'),(19,68,'2024-04-06 17:31:29'),(7,74,'2024-08-23 14:51:29'),(8,77,'2024-07-12 22:51:29'),(18,78,'2024-06-15 04:11:29'),(9,83,'2023-09-11 09:31:29'),(11,87,'2023-12-31 12:11:29'),(6,91,'2024-01-14 09:31:29'),(19,91,'2024-08-09 17:31:29'),(7,93,'2023-09-25 06:51:29'),(15,93,'2024-03-09 22:51:29'),(12,99,'2023-11-19 20:11:29');
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
  `Renk` varchar(100) NOT NULL,
  PRIMARY KEY (`HayvanID`,`Renk`),
  CONSTRAINT `renkler_ibfk_1` FOREIGN KEY (`HayvanID`) REFERENCES `hastahayvan` (`HastaID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `renkler`
--

LOCK TABLES `renkler` WRITE;
/*!40000 ALTER TABLE `renkler` DISABLE KEYS */;
INSERT INTO `renkler` VALUES (42,'kahverengi'),(43,'kırmızı'),(44,'sarı'),(45,'kahverengi'),(46,'mavi'),(47,'turuncu'),(48,'turuncu'),(49,'kahverengi'),(50,'kahverengi'),(51,'siyah'),(52,'sarı'),(53,'kırmızı'),(54,'kırmızı'),(55,'kahverengi'),(56,'siyah'),(57,'sarı'),(58,'beyaz'),(59,'turuncu'),(60,'beyaz'),(61,'sarı'),(62,'gri'),(63,'sarı'),(64,'turuncu'),(65,'turuncu'),(66,'beyaz'),(67,'siyah'),(68,'turuncu'),(69,'gri'),(70,'gri'),(71,'beyaz'),(72,'kahverengi'),(73,'kırmızı'),(74,'mavi'),(75,'beyaz'),(76,'mavi'),(77,'gri'),(78,'mavi'),(79,'kırmızı'),(80,'turuncu');
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
  `Açıklama` varchar(255) DEFAULT NULL,
  `Puan` int NOT NULL,
  PRIMARY KEY (`HayvanSahibiID`,`VeterinerID`),
  KEY `VeterinerID` (`VeterinerID`),
  CONSTRAINT `reviewverir_ibfk_1` FOREIGN KEY (`HayvanSahibiID`) REFERENCES `hayvansahibi` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reviewverir_ibfk_2` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviewverir`
--

LOCK TABLES `reviewverir` WRITE;
/*!40000 ALTER TABLE `reviewverir` DISABLE KEYS */;
INSERT INTO `reviewverir` VALUES (1,10,'culpa ex ad',1),(6,8,'maiores temporibus consequatur',5),(8,5,'omnis laborum autem',3),(9,4,'commodi ducimus maxime',9),(9,5,'ipsam dolorem reprehenderit',10),(12,0,'et quae nemo',1),(15,12,'maxime odio eius',9),(16,6,'necessitatibus modi ipsum',7),(17,5,'unde nisi quam',5),(21,7,'iste molestiae accusantium',9),(22,4,'architecto neque repudiandae',6),(26,2,'a natus repudiandae',8),(28,1,'atque eaque eos',1),(29,14,'unde corporis temporibus',7),(31,1,'culpa aliquam nihil',10),(34,11,'pariatur non dignissimos',4),(36,5,'exercitationem voluptates corrupti',8),(37,0,'facere officiis est',1),(37,2,'iusto eaque mollitia',1),(37,10,'beatae nisi placeat',4),(37,13,'praesentium earum possimus',2),(38,7,'mollitia voluptatum ad',8),(39,7,'sapiente neque perferendis',5),(41,15,'tenetur optio voluptatum',5),(42,0,'asperiores eligendi vitae',9),(42,3,'magni placeat sint',2),(43,0,'nisi ducimus placeat',10),(46,14,'eligendi soluta ipsa',8),(50,6,'repellat repellat voluptates',4),(53,13,'impedit occaecati itaque',3),(56,7,'nemo dolorem animi',6),(56,14,'nostrum quia accusantium',8),(60,3,'neque rerum repudiandae',4),(60,11,'deserunt quibusdam laboriosam',7),(67,4,'neque ab culpa',2),(69,13,'accusamus debitis voluptatibus',10),(76,15,'cupiditate libero velit',2),(78,3,'harum id odio',3),(78,4,'itaque tenetur maiores',1),(80,2,'numquam officiis odio',8);
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
  `Tarih` datetime DEFAULT NULL,
  `VeterinerID` int NOT NULL,
  `HastaHayvanID` int NOT NULL,
  PRIMARY KEY (`ReçeteID`),
  KEY `VeterinerID` (`VeterinerID`),
  KEY `HastaHayvanID` (`HastaHayvanID`),
  CONSTRAINT `reçete_ibfk_1` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `reçete_ibfk_2` FOREIGN KEY (`HastaHayvanID`) REFERENCES `hastahayvan` (`HastaID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reçete`
--

LOCK TABLES `reçete` WRITE;
/*!40000 ALTER TABLE `reçete` DISABLE KEYS */;
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-07-23T22:11:36.557', '20', '81');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-07-30T20:51:36.557', '11', '82');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-08-06T19:31:36.557', '17', '83');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-08-13T18:11:36.557', '18', '84');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-08-20T16:51:36.557', '14', '85');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-08-27T15:31:36.557', '16', '86');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-09-03T14:11:36.557', '6', '87');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-09-10T12:51:36.557', '10', '88');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-09-17T11:31:36.557', '8', '89');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-09-24T10:11:36.557', '7', '90');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-10-01T08:51:36.557', '18', '91');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-10-08T07:31:36.557', '7', '92');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-10-15T06:11:36.557', '7', '93');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-10-22T04:51:36.557', '12', '94');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-10-29T03:31:36.557', '7', '95');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-11-05T02:11:36.557', '13', '96');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-11-12T00:51:36.557', '17', '97');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-11-18T23:31:36.557', '11', '98');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-11-25T22:11:36.557', '14', '99');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-12-02T20:51:36.557', '6', '100');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-12-09T19:31:36.557', '10', '101');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-12-16T18:11:36.557', '20', '102');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-12-23T16:51:36.557', '17', '103');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2023-12-30T15:31:36.557', '13', '104');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-01-06T14:11:36.557', '18', '105');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-01-13T12:51:36.557', '14', '106');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-01-20T11:31:36.557', '17', '107');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-01-27T10:11:36.557', '11', '108');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-02-03T08:51:36.557', '7', '109');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-02-10T07:31:36.557', '13', '110');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-02-17T06:11:36.557', '10', '111');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-02-24T04:51:36.557', '13', '112');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-03-02T03:31:36.557', '18', '113');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-03-09T02:11:36.557', '7', '114');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-03-16T00:51:36.557', '16', '115');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-03-22T23:31:36.557', '11', '116');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-03-29T22:11:36.557', '12', '117');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-04-05T20:51:36.557', '17', '118');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-04-12T19:31:36.557', '18', '119');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-04-19T18:11:36.557', '13', '120');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-04-26T16:51:36.557', '17', '121');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-05-03T15:31:36.557', '6', '122');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-05-10T14:11:36.557', '11', '123');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-05-17T12:51:36.557', '19', '124');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-05-24T11:31:36.557', '19', '125');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-05-31T10:11:36.557', '11', '126');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-06-07T08:51:36.557', '15', '127');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-06-14T07:31:36.557', '20', '128');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-06-21T06:11:36.557', '14', '129');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-06-28T04:51:36.557', '6', '130');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-07-05T03:31:36.557', '11', '131');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-07-12T02:11:36.557', '17', '132');
INSERT INTO reçete (ReçeteID, Tarih, VeterinerID, HastaHayvanID) VALUES (null, '2024-07-19T00:51:36.557', '17', '133');
/*INSERT INTO `reçete` VALUES (3,'2020-07-07 04:18:07',8,16),(4,'2019-10-15 04:35:41',10,61),(5,'2071-07-30 18:24:35',18,6),(6,'2077-08-23 11:18:40',6,11),(7,'2064-12-18 04:59:30',19,32),(8,'2064-04-05 00:01:14',18,66),(9,'2066-01-26 06:25:30',20,12),(10,'2098-05-30 08:14:39',11,69),(11,'2034-11-12 02:25:36',19,18),(12,'2057-12-19 04:19:11',7,29),(13,'2015-06-29 15:21:28',17,42),(14,'2042-01-19 17:52:10',20,58),(15,'2028-07-12 14:21:44',15,79),(16,'2017-08-31 04:31:46',14,56),(17,'2092-01-04 19:31:59',11,46),(18,'2028-03-29 03:11:16',14,14),(19,'2026-05-02 19:55:28',20,20),(20,'2032-06-07 08:06:24',15,28),(21,'2013-10-08 03:08:35',17,29),(22,'2035-10-10 11:02:57',9,14),(23,'2096-10-13 04:30:34',13,41),(24,'1998-02-22 14:43:22',7,50),(25,'2008-01-07 15:12:16',15,33),(26,'2095-07-31 05:20:39',13,9),(27,'2089-10-16 13:31:01',14,18),(28,'2048-02-20 03:43:35',11,59),(29,'2038-11-17 09:13:13',11,51),(30,'2067-12-29 22:23:07',9,32),(31,'2086-12-31 02:49:06',19,24),(32,'2001-01-06 12:45:34',15,62),(33,'2007-01-25 07:12:02',20,54),(34,'2092-04-12 23:56:46',16,4),(35,'2038-03-24 12:07:24',13,68),(36,'2067-10-09 16:23:34',11,29),(37,'2090-06-04 06:04:51',9,37),(38,'2075-09-12 10:58:46',13,63),(39,'2004-04-19 08:42:00',7,16),(40,'2078-08-25 17:07:31',7,28),(41,'2086-12-21 11:58:07',7,5),(42,'2014-01-25 21:24:31',15,33),(43,'2020-11-11 04:08:29',13,54),(44,'2088-03-07 10:28:11',18,37),(45,'2004-03-11 04:18:41',16,77),(46,'2022-12-20 17:00:50',6,16),(47,'2026-01-07 13:25:25',20,21),(48,'2099-09-29 04:59:44',15,19),(49,'2048-11-13 17:12:36',10,16),(50,'2069-11-04 06:58:02',17,53),(51,'2093-11-15 09:30:09',6,58),(52,'2094-04-15 01:57:00',15,34),(53,'2006-04-20 01:36:54',9,38),(54,'2011-09-14 00:36:06',12,52),(55,'1993-04-02 20:52:32',15,24),(56,'2018-01-04 17:38:11',16,67),(57,'2094-07-27 23:00:47',8,57),(58,'2012-03-26 22:40:41',14,61),(59,'2080-07-30 20:48:06',13,4),(60,'2073-11-11 23:09:24',15,67),(61,'2059-04-02 13:42:25',8,54),(62,'2031-10-04 07:41:51',15,42),(63,'2061-03-17 22:01:45',11,80),(64,'2025-05-03 19:17:45',11,53),(65,'2001-11-29 13:39:50',10,25),(66,'2052-10-26 06:25:29',13,77),(67,'2013-01-06 02:31:58',12,17),(68,'2074-12-19 05:37:47',20,57),(69,'2016-07-30 16:12:08',18,16),(70,'2086-04-03 18:26:16',17,68),(71,'2055-02-17 01:49:25',8,37),(72,'2081-12-11 10:52:22',7,43),(73,'2051-08-07 02:02:54',11,66),(74,'2029-04-23 12:51:31',7,79),(75,'2018-01-30 14:50:42',7,13),(76,'2097-05-30 00:51:20',7,40),(77,'2065-07-10 11:25:54',11,17),(78,'2037-05-02 01:35:16',8,67),(79,'2086-11-02 22:33:36',18,76),(80,'2052-02-18 02:02:50',6,19),(81,'2044-02-06 14:33:23',7,44),(82,'2006-08-13 19:25:51',15,63),(83,'2074-03-03 00:29:11',18,67),(84,'2032-06-11 11:47:30',9,23),(85,'2045-04-18 00:49:15',16,75),(86,'2075-10-27 23:20:36',19,40),(87,'2015-01-14 03:48:59',16,64),(88,'2074-07-10 10:39:28',7,15),(89,'2030-01-05 14:14:10',19,31),(90,'2072-08-01 13:22:42',11,6),(91,'2076-05-29 03:20:31',6,25),(92,'2027-07-04 21:51:28',7,48),(93,'1998-08-14 20:42:01',19,18),(94,'2041-05-17 08:00:41',19,77),(95,'2047-03-01 21:50:29',20,46),(96,'2089-10-16 11:23:36',15,26),(97,'2058-10-26 07:39:18',20,8),(98,'2043-12-23 06:56:50',9,50),(99,'2013-08-21 20:33:59',19,67),(100,'1993-09-19 13:03:44',14,53),(101,'2095-05-04 04:53:35',11,48),(102,'2060-02-01 04:40:41',16,73);*/
/*!40000 ALTER TABLE `reçete` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `saatler`
--

LOCK TABLES `saatler` WRITE;
/*!40000 ALTER TABLE `saatler` DISABLE KEYS */;
INSERT INTO `saatler` VALUES (1,'Pazartesi',9,0),(2,'Pazartesi',9,10),(3,'Pazartesi',9,20),(4,'Pazartesi',9,30),(5,'Pazartesi',9,40),(6,'Pazartesi',9,50),(7,'Pazartesi',10,0),(8,'Pazartesi',10,10),(9,'Pazartesi',10,20),(10,'Pazartesi',10,30),(11,'Pazartesi',10,40),(12,'Pazartesi',10,50),(13,'Pazartesi',11,0),(14,'Pazartesi',11,10),(15,'Pazartesi',11,20),(16,'Pazartesi',11,30),(17,'Pazartesi',11,40),(18,'Pazartesi',11,50),(19,'Pazartesi',13,0),(20,'Pazartesi',13,10),(21,'Pazartesi',13,20),(22,'Pazartesi',13,30),(23,'Pazartesi',13,40),(24,'Pazartesi',13,50),(25,'Pazartesi',14,0),(26,'Pazartesi',14,10),(27,'Pazartesi',14,20),(28,'Pazartesi',14,30),(29,'Pazartesi',14,40),(30,'Pazartesi',14,50),(31,'Pazartesi',15,0),(32,'Pazartesi',15,10),(33,'Pazartesi',15,20),(34,'Pazartesi',15,30),(35,'Pazartesi',15,40),(36,'Pazartesi',15,50),(37,'Pazartesi',16,0),(38,'Pazartesi',16,10),(39,'Pazartesi',16,20),(40,'Pazartesi',16,30),(41,'Pazartesi',16,40),(42,'Pazartesi',16,50),(43,'Pazartesi',17,0),(44,'Pazartesi',17,10),(45,'Pazartesi',17,20),(46,'Pazartesi',17,30),(47,'Pazartesi',17,40),(48,'Pazartesi',17,50),(49,'Salı',9,0),(50,'Salı',9,10),(51,'Salı',9,20),(52,'Salı',9,30),(53,'Salı',9,40),(54,'Salı',9,50),(55,'Salı',10,0),(56,'Salı',10,10),(57,'Salı',10,20),(58,'Salı',10,30),(59,'Salı',10,40),(60,'Salı',10,50),(61,'Salı',11,0),(62,'Salı',11,10),(63,'Salı',11,20),(64,'Salı',11,30),(65,'Salı',11,40),(66,'Salı',11,50),(67,'Salı',13,0),(68,'Salı',13,10),(69,'Salı',13,20),(70,'Salı',13,30),(71,'Salı',13,40),(72,'Salı',13,50),(73,'Salı',14,0),(74,'Salı',14,10),(75,'Salı',14,20),(76,'Salı',14,30),(77,'Salı',14,40),(78,'Salı',14,50),(79,'Salı',15,0),(80,'Salı',15,10),(81,'Salı',15,20),(82,'Salı',15,30),(83,'Salı',15,40),(84,'Salı',15,50),(85,'Salı',16,0),(86,'Salı',16,10),(87,'Salı',16,20),(88,'Salı',16,30),(89,'Salı',16,40),(90,'Salı',16,50),(91,'Salı',17,0),(92,'Salı',17,10),(93,'Salı',17,20),(94,'Salı',17,30),(95,'Salı',17,40),(96,'Salı',17,50),(97,'Çarşamba',9,0),(98,'Çarşamba',9,10),(99,'Çarşamba',9,20),(100,'Çarşamba',9,30),(101,'Çarşamba',9,40),(102,'Çarşamba',9,50),(103,'Çarşamba',10,0),(104,'Çarşamba',10,10),(105,'Çarşamba',10,20),(106,'Çarşamba',10,30),(107,'Çarşamba',10,40),(108,'Çarşamba',10,50),(109,'Çarşamba',11,0),(110,'Çarşamba',11,10),(111,'Çarşamba',11,20),(112,'Çarşamba',11,30),(113,'Çarşamba',11,40),(114,'Çarşamba',11,50),(115,'Çarşamba',13,0),(116,'Çarşamba',13,10),(117,'Çarşamba',13,20),(118,'Çarşamba',13,30),(119,'Çarşamba',13,40),(120,'Çarşamba',13,50),(121,'Çarşamba',14,0),(122,'Çarşamba',14,10),(123,'Çarşamba',14,20),(124,'Çarşamba',14,30),(125,'Çarşamba',14,40),(126,'Çarşamba',14,50),(127,'Çarşamba',15,0),(128,'Çarşamba',15,10),(129,'Çarşamba',15,20),(130,'Çarşamba',15,30),(131,'Çarşamba',15,40),(132,'Çarşamba',15,50),(133,'Çarşamba',16,0),(134,'Çarşamba',16,10),(135,'Çarşamba',16,20),(136,'Çarşamba',16,30),(137,'Çarşamba',16,40),(138,'Çarşamba',16,50),(139,'Çarşamba',17,0),(140,'Çarşamba',17,10),(141,'Çarşamba',17,20),(142,'Çarşamba',17,30),(143,'Çarşamba',17,40),(144,'Çarşamba',17,50),(145,'Perşembe',9,0),(146,'Perşembe',9,10),(147,'Perşembe',9,20),(148,'Perşembe',9,30),(149,'Perşembe',9,40),(150,'Perşembe',9,50),(151,'Perşembe',10,0),(152,'Perşembe',10,10),(153,'Perşembe',10,20),(154,'Perşembe',10,30),(155,'Perşembe',10,40),(156,'Perşembe',10,50),(157,'Perşembe',11,0),(158,'Perşembe',11,10),(159,'Perşembe',11,20),(160,'Perşembe',11,30),(161,'Perşembe',11,40),(162,'Perşembe',11,50),(163,'Perşembe',13,0),(164,'Perşembe',13,10),(165,'Perşembe',13,20),(166,'Perşembe',13,30),(167,'Perşembe',13,40),(168,'Perşembe',13,50),(169,'Perşembe',14,0),(170,'Perşembe',14,10),(171,'Perşembe',14,20),(172,'Perşembe',14,30),(173,'Perşembe',14,40),(174,'Perşembe',14,50),(175,'Perşembe',15,0),(176,'Perşembe',15,10),(177,'Perşembe',15,20),(178,'Perşembe',15,30),(179,'Perşembe',15,40),(180,'Perşembe',15,50),(181,'Perşembe',16,0),(182,'Perşembe',16,10),(183,'Perşembe',16,20),(184,'Perşembe',16,30),(185,'Perşembe',16,40),(186,'Perşembe',16,50),(187,'Perşembe',17,0),(188,'Perşembe',17,10),(189,'Perşembe',17,20),(190,'Perşembe',17,30),(191,'Perşembe',17,40),(192,'Perşembe',17,50),(193,'Cuma',9,0),(194,'Cuma',9,10),(195,'Cuma',9,20),(196,'Cuma',9,30),(197,'Cuma',9,40),(198,'Cuma',9,50),(199,'Cuma',10,0),(200,'Cuma',10,10),(201,'Cuma',10,20),(202,'Cuma',10,30),(203,'Cuma',10,40),(204,'Cuma',10,50),(205,'Cuma',11,0),(206,'Cuma',11,10),(207,'Cuma',11,20),(208,'Cuma',11,30),(209,'Cuma',11,40),(210,'Cuma',11,50),(211,'Cuma',13,0),(212,'Cuma',13,10),(213,'Cuma',13,20),(214,'Cuma',13,30),(215,'Cuma',13,40),(216,'Cuma',13,50),(217,'Cuma',14,0),(218,'Cuma',14,10),(219,'Cuma',14,20),(220,'Cuma',14,30),(221,'Cuma',14,40),(222,'Cuma',14,50),(223,'Cuma',15,0),(224,'Cuma',15,10),(225,'Cuma',15,20),(226,'Cuma',15,30),(227,'Cuma',15,40),(228,'Cuma',15,50),(229,'Cuma',16,0),(230,'Cuma',16,10),(231,'Cuma',16,20),(232,'Cuma',16,30),(233,'Cuma',16,40),(234,'Cuma',16,50),(235,'Cuma',17,0),(236,'Cuma',17,10),(237,'Cuma',17,20),(238,'Cuma',17,30),(239,'Cuma',17,40),(240,'Cuma',17,50);
/*!40000 ALTER TABLE `saatler` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `uygundur`
--

LOCK TABLES `uygundur` WRITE;
/*!40000 ALTER TABLE `uygundur` DISABLE KEYS */;
INSERT INTO `uygundur` VALUES (12,6),(26,6),(90,6),(205,6),(43,7),(107,7),(158,7),(176,7),(72,8),(138,8),(122,9),(166,9),(184,9),(81,10),(144,10),(156,10),(212,10),(227,10),(89,11),(105,11),(235,11),(29,12),(147,12),(161,12),(229,12),(1,13),(119,13),(163,14),(223,14),(139,15),(237,15),(24,16),(48,16),(211,16),(8,17),(52,17),(212,17),(228,17),(2,18),(103,18),(186,18),(220,18),(36,19),(64,19),(91,19),(113,19),(200,19),(17,20),(55,20),(94,20);
/*!40000 ALTER TABLE `uygundur` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `veteriner`
--

LOCK TABLES `veteriner` WRITE;
/*!40000 ALTER TABLE `veteriner` DISABLE KEYS */;
INSERT INTO `veteriner` VALUES (6,'Shana','Osinski','62684296290','02128823745','Cambridgeshire','Renton','New Mexico',100,4),(7,'Clark','Brekke','76781094402','06087987071','Buckinghamshire','Brownsville','New Hampshire',101,2),(8,'Rosie','Beahan','12786421561','02721921773','Avon','Cicero','Minnesota',102,3),(9,'Filomena','Breitenberg','61155382526','00477543494','Cambridgeshire','Stockton','Connecticut',103,1),(10,'Lewis','Kuvalis','99161364550','06315429953','Berkshire','Dallas','Tennessee',104,5),(11,'Rickey','Stark','24724629388','06367756264','Berkshire','Lafayette','Nebraska',105,2),(12,'Antonio','Ziemann','36058979709','05710835032','Bedfordshire','Harrisburg','Kansas',106,1),(13,'Gerardo','Lubowitz','49067700890','05152682487','Cambridgeshire','Mishawaka','Maine',107,2),(14,'Charley','Hoppe','84582214642','02925354358','Borders','Highlands Ranch','Georgia',108,4),(15,'Mercedes','Denesik','32400956823','03581518530','Bedfordshire','Buckeye','Washington',109,2),(16,'Ludwig','Howe','55608945421','09967973372','Avon','Cranston','Arizona',110,2),(17,'Linnie','Douglas','64626621844','00287736608','Borders','St. Louis Park','Louisiana',111,1),(18,'Mallory','Weimann','53453307065','04670748970','Buckinghamshire','Shoreline','Kansas',112,4),(19,'Rhea','Marvin','48417487617','05392946672','Borders','Altoona','South Dakota',113,5),(20,'Era','Reichert','32660185618','09754509691','Berkshire','Raleigh','Idaho',114,4);
/*!40000 ALTER TABLE `veteriner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `yetkinlik`
--

DROP TABLE IF EXISTS `yetkinlik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `yetkinlik` (
  `VeterinerID` int NOT NULL,
  `Yetkinlik` enum('Kedi','Köpek','Kuş','Tavşan','Kaplumbağa','Hamster','Kobay') NOT NULL,
  primary key(VeterinerID,Yetkinlik),
  CONSTRAINT `temp` FOREIGN KEY (`VeterinerID`) REFERENCES `veteriner` (`KullanıcıID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `yetkinlik`
--

LOCK TABLES `yetkinlik` WRITE;
/*!40000 ALTER TABLE `yetkinlik` DISABLE KEYS */;
INSERT INTO `yetkinlik` VALUES (6,'Hamster'),(7,'Hamster'),(8,'Köpek'),(9,'Köpek'),(10,'Kobay'),(11,'Köpek'),(12,'Kuş'),(13,'Hamster'),(14,'Köpek'),(15,'Kobay'),(16,'Kobay'),(17,'Kuş'),(18,'Kaplumbağa'),(19,'Köpek'),(20,'Kedi'),(6,'Kobay'),(6,'Kedi'),(6,'Köpek'),(7,'Köpek'),(7,'Kedi'),(7,'Kuş'),(8,'Tavşan'),(8,'Kedi'),(8,'Kaplumbağa'),(9,'Kobay'),(10,'Kedi'),(11,'Tavşan'),(11,'Kuş'),(12,'Köpek'),(13,'Kuş'),(13,'Köpek'),(14,'Kobay'),(15,'Köpek'),(15,'Kaplumbağa'),(15,'Kedi'),(16,'Kedi'),(16,'Kuş'),(16,'Kaplumbağa'),(17,'Tavşan'),(18,'Köpek'),(19,'Tavşan'),(19,'Kedi'),(20,'Tavşan');
/*!40000 ALTER TABLE `yetkinlik` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-23 17:59:26