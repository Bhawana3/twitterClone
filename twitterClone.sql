-- MySQL dump 10.13  Distrib 5.6.28, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: twitter_clone
-- ------------------------------------------------------
-- Server version	5.6.28-0ubuntu0.15.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `followers` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  UNIQUE KEY `follower_id` (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`uid`),
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
INSERT INTO `followers` VALUES (3,1),(9,1),(32,1),(34,1),(1,3),(32,3),(34,3),(37,3),(1,23),(32,23),(1,24),(3,24),(32,24),(34,24),(1,25),(32,25),(3,32),(1,34),(3,34),(32,34),(3,37),(32,37);
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_tweets`
--

DROP TABLE IF EXISTS `user_tweets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_tweets` (
  `t_id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `tweet` varchar(200) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `changed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`t_id`),
  KEY `uid` (`uid`),
  CONSTRAINT `user_tweets_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_tweets`
--

LOCK TABLES `user_tweets` WRITE;
/*!40000 ALTER TABLE `user_tweets` DISABLE KEYS */;
INSERT INTO `user_tweets` VALUES (6,25,'hello','2016-05-28 08:57:07','2016-05-28 08:57:07'),(7,3,'ansdjhj','2016-05-28 19:51:08','2016-05-28 19:51:08'),(8,3,'alkskjadjforwoa','2016-05-28 19:51:14','2016-05-28 19:51:14'),(9,3,'ndkjsnlaljifka','2016-05-28 19:51:19','2016-05-28 19:51:19'),(10,3,'szndlfsjjlalkfsa','2016-05-28 19:51:26','2016-05-28 19:51:26'),(11,3,'sfdkhkethg','2016-05-29 10:18:51','2016-05-29 10:18:51'),(12,32,'Nothing is on my mind','2016-05-29 10:27:43','2016-05-29 10:27:43'),(13,3,'hello world','2016-05-29 11:35:59','2016-05-29 11:35:59'),(15,32,'I want to change my picture','2016-05-29 18:41:09','2016-05-29 18:41:09'),(16,32,'Fix the bug on Search page','2016-05-29 18:43:14','2016-05-29 18:43:14'),(17,32,'After logging out, back button takes back to the profile page. fix this.','2016-05-29 18:43:54','2016-05-29 18:43:54'),(18,32,'Add links to user profiles.','2016-05-29 18:44:43','2016-05-29 18:44:43'),(19,32,'Option to Delete tweet','2016-05-29 18:47:55','2016-05-29 18:47:55'),(20,32,'Think of a better algorithm for home page (optional)','2016-05-29 18:48:30','2016-05-29 18:48:30'),(21,32,'Think of some method to support hashtags (optional).','2016-05-29 18:50:18','2016-05-29 18:50:18'),(29,3,'fghghgg','2016-06-01 15:06:35','2016-06-01 15:06:35'),(30,3,'It\'s Raining!!!','2016-06-02 07:20:01','2016-06-02 07:20:01'),(33,24,'Hello.','2016-06-03 08:01:44','2016-06-03 08:01:44'),(34,24,'Hi. Uploading photo.','2016-06-03 08:02:09','2016-06-03 08:02:09'),(35,32,'@bhawana: There should be a feature to preview profile pictures of others.','2016-06-03 08:10:07','2016-06-03 08:10:07'),(36,34,'Morning sunshine :-)','2016-06-04 08:19:46','2016-06-04 08:19:46'),(37,37,'nothing on my mind bitch !','2016-06-05 16:47:25','2016-06-05 16:47:25'),(38,32,'@bhawana: On \'home page\' cursor on tweet icon is still \'+\' sign.','2016-06-06 09:40:36','2016-06-06 09:40:36'),(62,1,'helllo!!!!!!','2016-06-06 11:21:09','2016-06-06 11:21:09');
/*!40000 ALTER TABLE `user_tweets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(100) NOT NULL,
  `profile_pic` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'bhawana','vermabhawana50@gmail.com','abc','uploads/1.jpg'),(3,'Bhawana','bhawana@qtos.in','abc','uploads/3.JPG'),(9,'anamika','bhawana.verma.iitr@gmail.com','123',NULL),(23,'Piyush Madan','abc@gmail.com','123',NULL),(24,'apratimganguli','apratim@qtos.in','abc','uploads/24.jpg'),(25,'apratimganguli','apratimganguli@gmail.com','abc',NULL),(30,'Piyush','abcd@gmail.com','abc',NULL),(32,'Piyush','piyushmadan2009@gmail.com','abc','uploads/32.gif'),(34,'smrom','sumitmalikinrome@gmail.com','Ying&*','uploads/34.JPG'),(37,'harsimran','kaur.harsimran301@gmail.com','harsimran','uploads/37.JPG');
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

-- Dump completed on 2016-06-07  0:21:57
