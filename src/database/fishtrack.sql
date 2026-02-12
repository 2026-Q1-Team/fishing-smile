-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 11, 2026 at 09:19 AM
-- Server version: 5.7.24
-- PHP Version: 8.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fishtrack`
--

-- --------------------------------------------------------

--
-- Table structure for table `fishcast`
--

CREATE TABLE `fishcast` (
  `uid` int(11) NOT NULL,
  `urc` varchar(32) NOT NULL,
  `scheme` varchar(32) NOT NULL,
  `target` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `fishcook`
--

CREATE TABLE `fishcook` (
  `uid` int(11) NOT NULL,
  `atk_id` int(11) NOT NULL,
  `component` varchar(64) DEFAULT NULL,
  `ts` datetime NOT NULL,
  `action` varchar(64) NOT NULL,
  `detail` json NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `fishlist`
--

CREATE TABLE `fishlist` (
  `uid` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  `email` varchar(64) NOT NULL,
  `phone` varchar(16) NOT NULL,
  `company` varchar(64) NOT NULL,
  `jobtitle` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fishcast`
--
ALTER TABLE `fishcast`
  ADD PRIMARY KEY (`uid`),
  ADD KEY `fk_target1` (`target`);

--
-- Indexes for table `fishcook`
--
ALTER TABLE `fishcook`
  ADD PRIMARY KEY (`uid`),
  ADD KEY `fk_atk_id1` (`atk_id`);

--
-- Indexes for table `fishlist`
--
ALTER TABLE `fishlist`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fishcast`
--
ALTER TABLE `fishcast`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fishcook`
--
ALTER TABLE `fishcook`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fishlist`
--
ALTER TABLE `fishlist`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fishcast`
--
ALTER TABLE `fishcast`
  ADD CONSTRAINT `fk_target1` FOREIGN KEY (`target`) REFERENCES `fishlist` (`uid`);

--
-- Constraints for table `fishcook`
--
ALTER TABLE `fishcook`
  ADD CONSTRAINT `fk_atk_id1` FOREIGN KEY (`atk_id`) REFERENCES `fishcast` (`uid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
