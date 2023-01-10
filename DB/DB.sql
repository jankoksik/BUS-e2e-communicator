-- Adminer 4.8.1 MySQL 8.0.17 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE TABLE `MSG` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(32) NOT NULL,
  `reciver` varchar(32) NOT NULL,
  `encoded_to` varchar(32)  NOT NULL,
  `send_time` datetime NOT NULL,
  `msg` varchar(32) NOT NULL,
  `Opened` BOOLEAN Not NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `PublicKey` varchar(3000) NOT NULL,
  `AvatarUrl` VARCHAR(400) Not NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- 2022-10-31 12:17:08
