-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema movie
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema movie
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movie` DEFAULT CHARACTER SET utf8 ;
USE `movie` ;

-- -----------------------------------------------------
-- Table `movie`.`movie`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`movie` (
  `MovieID` INT NOT NULL,
  `CName` CHAR(50) NULL,
  `EName` CHAR(50) NULL,
  `Type` CHAR(20) NULL,
  `Length` INT NULL,
  `ReleaseTime` INT NULL,
  `Standard` CHAR(30) NULL,
  `SumBoxOffice` INT NULL,
  `AvgPrice` INT NULL,
  `AvgPeople` INT NULL,
  `WomIndex` FLOAT NULL,
  PRIMARY KEY (`MovieID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`actor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`actor` (
  `ActorID` INT NOT NULL,
  `CName` CHAR(20) NULL,
  `EName` CHAR(20) NULL,
  `Nation` CHAR(20) NULL,
  PRIMARY KEY (`ActorID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`movie_actor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`movie_actor` (
  `MovieID` INT NOT NULL,
  `ActorID` INT NOT NULL,
  `Rank` INT NULL,
  `Role` CHAR(10) NOT NULL,
  PRIMARY KEY (`MovieID`, `ActorID`),
  INDEX `fk_movie_has_actor_actor1_idx` (`ActorID` ASC),
  INDEX `fk_movie_has_actor_movie_idx` (`MovieID` ASC),
  CONSTRAINT `fk_movie_has_actor_movie`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movie`.`movie` (`MovieID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_has_actor_actor1`
    FOREIGN KEY (`ActorID`)
    REFERENCES `movie`.`actor` (`ActorID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`movie_boxoffice`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`movie_boxoffice` (
  `MovieID` INT NOT NULL,
  `Date` INT NOT NULL,
  `BoxOffice` INT NULL,
  `AvgPeople` INT NULL,
  PRIMARY KEY (`MovieID`),
  CONSTRAINT `fk_movie_boxoffice_movie1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movie`.`movie` (`MovieID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`movie_scene`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`movie_scene` (
  `MovieID` INT NOT NULL,
  `CityID` INT NOT NULL,
  `Date` INT NOT NULL,
  `Scene` INT NULL,
  PRIMARY KEY (`MovieID`, `CityID`),
  INDEX `fk_table2_movie1_idx` (`MovieID` ASC),
  CONSTRAINT `fk_table2_movie1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movie`.`movie` (`MovieID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`city_cinema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`city_cinema` (
  `CityID` INT NOT NULL,
  `CinemaID` CHAR(50) NULL,
  PRIMARY KEY (`CityID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`city`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`city` (
  `CityID` INT NOT NULL,
  `Name` CHAR(30) NULL,
  `CinemaSum` INT NULL,
  PRIMARY KEY (`CityID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`cinema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`cinema` (
  `CinemaID` INT NOT NULL,
  `CityID` INT NOT NULL,
  `Name` VARCHAR(45) NULL,
  `Address` VARCHAR(45) NULL,
  `SitSum` INT NULL,
  PRIMARY KEY (`CinemaID`),
  INDEX `fk_cinema_city1_idx` (`CityID` ASC),
  CONSTRAINT `fk_cinema_city1`
    FOREIGN KEY (`CityID`)
    REFERENCES `movie`.`city` (`CityID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`movie_cinema`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`movie_cinema` (
  `MovieID` INT NOT NULL,
  `CinemaID` INT NOT NULL,
  `Date` INT NOT NULL,
  `Scene` INT NULL,
  `SumBoxOffice` INT NULL,
  `SumPeople` INT NULL,
  PRIMARY KEY (`MovieID`, `CinemaID`, `Date`),
  INDEX `fk_movie_has_cinema_cinema1_idx` (`CinemaID` ASC),
  INDEX `fk_movie_has_cinema_movie1_idx` (`MovieID` ASC),
  CONSTRAINT `fk_movie_has_cinema_movie1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movie`.`movie` (`MovieID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_has_cinema_cinema1`
    FOREIGN KEY (`CinemaID`)
    REFERENCES `movie`.`cinema` (`CinemaID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`company` (
  `CompanyID` INT NOT NULL,
  `CName` CHAR(30) NULL,
  `EName` CHAR(30) NULL,
  `Nation` CHAR(10) NULL,
  PRIMARY KEY (`CompanyID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movie`.`movie_company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movie`.`movie_company` (
  `MovieID` INT NOT NULL,
  `CompanyID` INT NOT NULL,
  `Rank` INT NULL,
  `Role` CHAR(10) NOT NULL,
  PRIMARY KEY (`MovieID`, `CompanyID`),
  INDEX `fk_movie_has_producer_producer1_idx` (`CompanyID` ASC),
  INDEX `fk_movie_has_producer_movie1_idx` (`MovieID` ASC),
  CONSTRAINT `fk_movie_has_producer_movie1`
    FOREIGN KEY (`MovieID`)
    REFERENCES `movie`.`movie` (`MovieID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movie_has_producer_producer1`
    FOREIGN KEY (`CompanyID`)
    REFERENCES `movie`.`company` (`CompanyID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
