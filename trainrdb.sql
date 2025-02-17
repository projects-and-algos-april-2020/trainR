-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema trainrdb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `trainrdb` ;

-- -----------------------------------------------------
-- Schema trainrdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `trainrdb` DEFAULT CHARACTER SET utf8 ;
USE `trainrdb` ;

-- -----------------------------------------------------
-- Table `trainrdb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trainrdb`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL,
  `last_name` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `adminlevel` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trainrdb`.`user_workout`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trainrdb`.`user_workout` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `set_num` INT NULL,
  `rep` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_user_workout_user_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_workout_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `trainrdb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `trainrdb`.`user_suggestions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trainrdb`.`user_suggestions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `suggestion` TEXT NULL,
  `reply` TEXT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_user_suggestions_user1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_suggestions_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `trainrdb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
