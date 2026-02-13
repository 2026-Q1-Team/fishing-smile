-- This SQL file is used only to create database and tables.

-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Feb 12, 2026 at 07:53 AM
-- Server version: 9.6.0
-- PHP Version: 8.3.30


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fishtrack`
--
CREATE DATABASE IF NOT EXISTS `fishtrack`;
USE `fishtrack`;


CREATE TABLE IF NOT EXISTS `Target Profile` (
  `uid` int NOT NULL,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `company` varchar(64) NOT NULL,
  `JobTitle` varchar(64) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `Attack` (
  `uid` int NOT NULL,
  `UniqueRandomCode` varchar(32) DEFAULT NULL,
  `scheme` varchar(32) NOT NULL,
  `target` int NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE IF NOT EXISTS `Event` (
  `uid` int NOT NULL,
  `atk_id` int NOT NULL,
  `kind` varchar(64) DEFAULT NULL,
  `ts` datetime NOT NULL,
  `detail` json NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


--
-- Indexes for dumped tables
--

--
-- Indexes for table `Attack`
--
ALTER TABLE `Attack`
  ADD KEY `fk_target1` (`target`);

--
-- Indexes for table `Event`
--
ALTER TABLE `Event`
  ADD KEY `fk_atk_id1` (`atk_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Attack`
--
ALTER TABLE `Attack`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Event`
--
ALTER TABLE `Event`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Target Profile`
--
ALTER TABLE `Target Profile`
  MODIFY `uid` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Attack`
--
ALTER TABLE `Attack`
  ADD CONSTRAINT `Attack_ibfk_1` FOREIGN KEY (`target`) REFERENCES `Target Profile` (`uid`) ON DELETE CASCADE;

--
-- Constraints for table `Event`
--
ALTER TABLE `Event`
  ADD CONSTRAINT `Event_ibfk_1` FOREIGN KEY (`atk_id`) REFERENCES `Attack` (`uid`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
