-- This SQL file defines schema for `fishtrack` database

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;


CREATE DATABASE IF NOT EXISTS `fishtrack`;
USE `fishtrack`;


CREATE TABLE IF NOT EXISTS `TargetProfile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `company` varchar(64) DEFAULT NULL,
  `job_title` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `Attack` (
  `id` int NOT NULL AUTO_INCREMENT,
  `external_id` char(32) NOT NULL,
  `scheme` varchar(32) NOT NULL,
  `target` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`external_id`),
  FOREIGN KEY (`target`) REFERENCES `TargetProfile` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `Event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `parent_attack` int DEFAULT NULL,
  `kind` varchar(64) NOT NULL,
  `time` datetime NOT NULL,
  `detail` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`parent_attack`) REFERENCES `Attack` (`id`)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
