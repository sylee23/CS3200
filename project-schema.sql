CREATE DATABASE  IF NOT EXISTS `project` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `project`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: project
-- ------------------------------------------------------
-- Server version	5.7.19-log

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
-- Table structure for table `co_ops`
--

DROP TABLE IF EXISTS `co_ops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `co_ops` (
  `start` date NOT NULL,
  `end` date DEFAULT NULL,
  `user_username` varchar(30) NOT NULL,
  `company` varchar(45) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`start`,`user_username`),
  KEY `fk_co-ops_user1_idx` (`user_username`),
  CONSTRAINT `fk_co-ops_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `connections`
--

DROP TABLE IF EXISTS `connections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `connections` (
  `owner` varchar(30) NOT NULL,
  `connected` varchar(30) NOT NULL,
  PRIMARY KEY (`owner`,`connected`),
  KEY `fk_user_has_user_user2_idx` (`connected`),
  KEY `fk_user_has_user_user1_idx` (`owner`),
  CONSTRAINT `fk_user_has_user_user1` FOREIGN KEY (`owner`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_user_user2` FOREIGN KEY (`connected`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course` (
  `idcourse` int(11) NOT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `professor` varchar(45) DEFAULT NULL,
  `semester` date DEFAULT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`idcourse`,`user_username`),
  KEY `fk_course_user1_idx` (`user_username`),
  CONSTRAINT `fk_course_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_admin`
--

DROP TABLE IF EXISTS `group_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_admin` (
  `group_idgroup` int(11) NOT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`group_idgroup`,`user_username`),
  KEY `fk_group_has_user1_user1_idx` (`user_username`),
  KEY `fk_group_has_user1_group1_idx` (`group_idgroup`),
  CONSTRAINT `fk_group_has_user1_group1` FOREIGN KEY (`group_idgroup`) REFERENCES `groups` (`idgroup`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_group_has_user1_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `group_users`
--

DROP TABLE IF EXISTS `group_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_users` (
  `group_idgroup` int(11) NOT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`group_idgroup`,`user_username`),
  KEY `fk_group_has_user_user1_idx` (`user_username`),
  KEY `fk_group_has_user_group_idx` (`group_idgroup`),
  CONSTRAINT `fk_group_has_user_group` FOREIGN KEY (`group_idgroup`) REFERENCES `groups` (`idgroup`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_group_has_user_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `idgroup` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `description` text,
  `picture` blob,
  PRIMARY KEY (`idgroup`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `major`
--

DROP TABLE IF EXISTS `major`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `major` (
  `name` varchar(45) NOT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`name`,`user_username`),
  KEY `fk_Major_user1_idx` (`user_username`),
  CONSTRAINT `fk_Major_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `minor`
--

DROP TABLE IF EXISTS `minor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `minor` (
  `name` varchar(45) NOT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`name`,`user_username`),
  KEY `fk_minor_user1_idx` (`user_username`),
  CONSTRAINT `fk_minor_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `research`
--

DROP TABLE IF EXISTS `research`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `research` (
  `start` date DEFAULT NULL,
  `end` date DEFAULT NULL,
  `professor` varchar(45) NOT NULL,
  `description` text,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`professor`,`user_username`),
  KEY `fk_research_user1_idx` (`user_username`),
  CONSTRAINT `fk_research_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `study_abroad`
--

DROP TABLE IF EXISTS `study_abroad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `study_abroad` (
  `country` varchar(45) DEFAULT NULL,
  `start` date NOT NULL,
  `end` date DEFAULT NULL,
  `university` varchar(45) DEFAULT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`user_username`,`start`),
  KEY `fk_study_abroad_user1_idx` (`user_username`),
  CONSTRAINT `fk_study_abroad_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tag_group`
--

DROP TABLE IF EXISTS `tag_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_group` (
  `name` varchar(45) NOT NULL,
  `group_idgroup` int(11) NOT NULL,
  PRIMARY KEY (`name`,`group_idgroup`),
  KEY `fk_tag_group_group1_idx` (`group_idgroup`),
  CONSTRAINT `fk_tag_group_group1` FOREIGN KEY (`group_idgroup`) REFERENCES `groups` (`idgroup`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tag_user`
--

DROP TABLE IF EXISTS `tag_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_user` (
  `name` varchar(45) NOT NULL,
  `user_username` varchar(30) NOT NULL,
  PRIMARY KEY (`name`,`user_username`),
  KEY `fk_tagUser_user1_idx` (`user_username`),
  CONSTRAINT `fk_tagUser_user1` FOREIGN KEY (`user_username`) REFERENCES `users` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `username` varchar(30) NOT NULL,
  `password` varchar(45) DEFAULT NULL,
  `Name` varchar(45) DEFAULT NULL,
  `Description` text,
  `gradYear` int(11) DEFAULT NULL,
  `Picture` blob,
  `email` varchar(45) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-25 20:00:50
