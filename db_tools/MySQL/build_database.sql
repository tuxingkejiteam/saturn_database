CREATE DATABASE `Saturn_Database_V1`;
USE `Saturn_Database_V1`;

CREATE TABLE `MD5对照表`(
  `MD5` CHAR(32),
  `UC` CHAR(7),
  PRIMARY KEY (`md5`),
  UNIQUE KEY (`uc`)
);

CREATE TABLE `编码使用记录表`(
  `日期编码` CHAR(3),
  `已使用数量` INT,
  PRIMARY KEY (`日期编码`)
);

CREATE TABLE `标签信息表`(
  `标签` CHAR(20),
  `大类` CHAR(10) NOT NULL,
  `部件` CHAR(20) NOT NULL,
  `描述` CHAR(20) NOT NULL,
  `特殊` BOOL NOT NULL,
  `更新日期` INT DEFAULT 191111,
  PRIMARY KEY(`标签`)
  );
  
  
CREATE TABLE `图片大类表` (
  `唯一编码` CHAR(7),
  `输配变` CHAR(1) DEFAULT NULL,
  `电压等级` CHAR(6) DEFAULT NULL,
  `含有缺陷` BOOL DEFAULT NULL,
  `历史遗留` BOOL DEFAULT NULL,
  `可见光` BOOL DEFAULT TRUE,
  `裸图` BOOL DEFAULT NULL,
  `野外` BOOL DEFAULT NULL,
  `绝缘子` BOOL DEFAULT NULL,
  `金具` BOOL DEFAULT NULL,
  `导线` BOOL DEFAULT NULL,
  `安监` BOOL DEFAULT NULL,
  `附属设施` BOOL DEFAULT NULL,
  `人体` BOOL DEFAULT NULL,
  `塔基` BOOL DEFAULT NULL,
  `异物` BOOL DEFAULT NULL,
  `其他` BOOL DEFAULT NULL,
  PRIMARY KEY (`唯一编码`)
  );

CREATE TABLE `标签信息表`(
  `标签` VARCHAR(20),
  `大类` VARCHAR(10) NOT NULL,
  `部件` VARCHAR(20) NOT NULL,
  `描述` VARCHAR(20) NOT NULL,
  `特殊` BOOL NOT NULL,
  `更新日期` CHAR(6) DEFAULT '191111',
  PRIMARY KEY(`标签`)
  );
