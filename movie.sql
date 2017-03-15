/*
Navicat MySQL Data Transfer

Source Server         : 11111
Source Server Version : 50628
Source Host           : localhost:3306
Source Database       : movie

Target Server Type    : MYSQL
Target Server Version : 50628
File Encoding         : 65001

Date: 2017-03-08 18:22:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for actor
-- ----------------------------
DROP TABLE IF EXISTS `actor`;
CREATE TABLE `actor` (
  `ActorID` int(11) NOT NULL AUTO_INCREMENT,
  `CName` char(50) DEFAULT NULL,
  `EName` char(50) DEFAULT NULL,
  `Type` char(50) DEFAULT NULL,
  PRIMARY KEY (`ActorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for city_cinema
-- ----------------------------
DROP TABLE IF EXISTS `city_cinema`;
CREATE TABLE `city_cinema` (
  `City` char(50) NOT NULL,
  `Cinema` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`City`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `MovieID` int(11) NOT NULL AUTO_INCREMENT,
  `CName` char(50) DEFAULT NULL,
  `EName` char(50) DEFAULT NULL,
  `Type` char(50) DEFAULT NULL,
  `Length` int(11) DEFAULT NULL,
  `ReleaseTime` int(11) DEFAULT NULL,
  `Standard` char(50) DEFAULT NULL,
  `Director` char(50) DEFAULT NULL,
  `ProductionCompany` varchar(255) DEFAULT NULL,
  `Publisher` varchar(255) DEFAULT NULL,
  `SumBoxOffice` int(11) DEFAULT NULL,
  `AvgPrice` int(11) DEFAULT NULL,
  `AvgPeople` int(11) DEFAULT NULL,
  `WomIndex` float DEFAULT NULL,
  `MovieDay` int(11) DEFAULT NULL,
  PRIMARY KEY (`MovieID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for movie_actor
-- ----------------------------
DROP TABLE IF EXISTS `movie_actor`;
CREATE TABLE `movie_actor` (
  `MovieID` int(11) NOT NULL,
  `ActorID` int(11) NOT NULL,
  PRIMARY KEY (`MovieID`,`ActorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for movie_boxoffice
-- ----------------------------
DROP TABLE IF EXISTS `movie_boxoffice`;
CREATE TABLE `movie_boxoffice` (
  `MovieID` int(11) NOT NULL,
  `Date` int(11) DEFAULT NULL,
  `BoxOffice` int(11) DEFAULT NULL,
  PRIMARY KEY (`MovieID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for movie_scene
-- ----------------------------
DROP TABLE IF EXISTS `movie_scene`;
CREATE TABLE `movie_scene` (
  `MovieID` int(11) NOT NULL,
  `City` char(50) DEFAULT NULL,
  `Date` int(11) DEFAULT NULL,
  `Scene` int(11) DEFAULT NULL,
  PRIMARY KEY (`MovieID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
