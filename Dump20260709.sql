-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: smartcart_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'yogi','chinniyugandhar996@gmail.com','$2b$12$yhoJopSmQpAT.7WQIp4ndem4K9eYV7FlJz6QnZcqxChL2VzCRl9de','picture.jpeg');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(200) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`),
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,1,8,'Mac Book',1,199999.00),(2,2,10,'dress',1,999.00),(3,3,9,'Samsung S26',1,149999.00),(4,4,8,'Mac Book',1,199999.00),(5,5,8,'Mac Book',1,199999.00),(6,6,15,'Villain',1,4999.00),(7,7,11,'T- shirts',1,777.00),(8,8,10,'dress',1,999.00),(9,9,8,'Mac Book',1,199999.00),(10,10,8,'Mac Book',1,199999.00),(11,11,8,'Mac Book',1,199999.00),(12,12,10,'dress',1,999.00),(13,13,10,'dress',1,999.00),(14,14,10,'dress',1,999.00),(15,15,17,'Half saree',1,1999.00),(16,16,8,'Mac Book',1,199999.00),(17,17,17,'Half saree',1,99.00),(18,18,9,'Samsung S26',1,149999.00),(19,19,8,'Mac Book',1,199999.00);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `razorpay_order_id` varchar(100) DEFAULT NULL,
  `razorpay_payment_id` varchar(100) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_status` varchar(30) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'order_T8xwsBPvxw69GR','pay_T8xx7sBIOZLavP',199999.00,'paid','2026-07-03 08:36:21'),(2,1,'order_T8y8hzrVldufdV','pay_T8y8sEeloyl9z4',999.00,'paid','2026-07-03 08:47:27'),(3,1,'order_T8yD2PRscDjmtd','pay_T8yDC11xyXIvt0',149999.00,'paid','2026-07-03 08:51:32'),(4,1,'order_T8yNLL0vlkTDdv','pay_T8yNUSm9Hkknjb',199999.00,'paid','2026-07-03 09:01:18'),(5,1,'order_T8yO8Ol2MnY0od','pay_T8yOHP4WmUWsZ0',199999.00,'paid','2026-07-03 09:02:07'),(6,1,'order_T8ybc1KHly7e5L','pay_T8ybqqmTtebxpj',4999.00,'paid','2026-07-03 09:14:54'),(7,1,'order_T8ypRuEnYl3oBN','pay_T8ypdvxC3jO2yJ',777.00,'paid','2026-07-03 09:27:56'),(8,1,'order_T8ytxFgAihwTGg','pay_T8yu8liJAaU1fo',999.00,'paid','2026-07-03 09:32:12'),(9,1,'order_T9KwKfJskWtlwQ','pay_T9KwYIevgwnCAW',199999.00,'paid','2026-07-04 07:05:44'),(10,1,'order_T9QOuads7JOy90','pay_T9QPD2YfdPWIij',199999.00,'paid','2026-07-04 12:26:24'),(11,1,'order_T9SlmWd0XkyaWF','pay_T9Sm2p7RQVibgs',199999.00,'paid','2026-07-04 14:45:20'),(12,1,'order_T9Snfti0x45nB5','pay_T9SnrsHNACJIBY',999.00,'paid','2026-07-04 14:47:07'),(13,1,'order_TA6rcNTRGjhDxC','pay_TA6ry4NtCKpz1N',999.00,'paid','2026-07-06 05:58:46'),(14,1,'order_TA9pznw9tGtN79','pay_TA9qFMQq0Hna0g',999.00,'paid','2026-07-06 08:53:10'),(15,1,'order_TAVP2myviEHmWE','pay_TAVPSIbKtj9JnO',1999.00,'paid','2026-07-07 05:59:04'),(16,1,'order_TAWh3Xpnq7Mfa8','pay_TAWhLDxKEAAAeU',199999.00,'paid','2026-07-07 07:14:46'),(17,1,'order_TAe9Xnh3OWssdc','pay_TAe9kNRkxTWRJe',99.00,'paid','2026-07-07 14:32:26'),(18,1,'order_TB0sEzFJMwFgP2','pay_TB0sSE8r5ZQnQ3',149999.00,'paid','2026-07-08 12:45:59'),(19,1,'order_TB2N7zVoG3B0Pg','pay_TB2NKPToUZx0Um',199999.00,'paid','2026-07-08 14:13:58');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) DEFAULT NULL,
  `description` text,
  `category` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (8,'Mac Book','MacBook is Apple’s stylish, high-performance laptop series for everyday use and professional work.','Electronics',199999.00,'Mac_Book.jpeg'),(9,'Samsung S26','Samsung S26 is a compact premium phone with a bright 120Hz AMOLED display, strong cameras, long software support, and Samsung’s Galaxy AI features.','Electronics',149999.00,'Samsung_S26.jpeg'),(10,'dress','available more colors','clothes',999.00,'Womens_Floral_Print_Midi_Dress_Navy_Blue_with_White_Leaves_Pattern.jpeg'),(11,'T- shirts','available in more colors ','clothes',777.00,'3pcs_Pack_Mens_Summer_Knitted_Solid_Color_Casual_Short_Sleeve_T-Shirt.jpeg'),(12,'Boat Airpods','good sound quality dolby experience','Electronics',1999.00,'Boat_Airdopes_Ace_Gen_2_TWS.jpeg'),(13,'Apple debuts','high procesing speed latest version','Electronics',99999.00,'Apple_debuts_its_799_iPhone_13_including_new_PINK_color_option.jpeg'),(14,'Guitar','muaic instrument good sound','music Instruments',3999.00,'download.jpeg'),(15,'Villain','good sound','music Instruments',4999.00,'download_1.jpeg'),(16,'half saree','available','clothes',1999.00,'Half_Saree.jpeg'),(17,'Half saree','it is available in different colors and models better for traditional look outfit','clothes',99.00,'Half_Saree.jpeg');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `address` text,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  `profile_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Chinni','chinniyugandhar996@gmail.com','$2b$12$2z4A7YFbR0B8GrzjXf7fU.9SLsHzG9oiQiUtBNCJ2HFFtqb68Op/K','7993275944','','Gopalapuram','','534316','picture.jpeg');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-09 22:35:41
