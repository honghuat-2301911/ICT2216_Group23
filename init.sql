-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `password` VARCHAR(225) NOT NULL,
  `email` VARCHAR(225) NOT NULL,
  `skill_lvl` VARCHAR(45) NULL,
  `sports_exp` VARCHAR(45) NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`sports_activity`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`sports_activity` (
  `id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `activity_name` VARCHAR(225) NOT NULL,
  `activity_type` VARCHAR(225) NOT NULL,
  `skills_req` VARCHAR(225) NOT NULL,
  `date` DATETIME NOT NULL,
  `location` VARCHAR(225) NOT NULL,
  `max_pax` INT NOT NULL,
  `user_id_list_join` VARCHAR(225) NULL,
  PRIMARY KEY (`id`, `date`),
  INDEX `fk_user_id_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- feed table
CREATE TABLE IF NOT EXISTS `mydb`.`feed` (
  `id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `image` MEDIUMBLOB NULL,
  `caption` VARCHAR(45) NULL,
  `like_count` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_feed_user_id` (`user_id`),
  CONSTRAINT `fk_feed_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- comments table
CREATE TABLE IF NOT EXISTS `mydb`.`comments` (
  `id` INT NOT NULL,
  `feed_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `comments` VARCHAR(225) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_comments_user_id` (`user_id`),
  INDEX `idx_comments_feed_id` (`feed_id`),
  CONSTRAINT `fk_comments_feed`
    FOREIGN KEY (`feed_id`)
    REFERENCES `mydb`.`feed` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comments_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `mydb`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
