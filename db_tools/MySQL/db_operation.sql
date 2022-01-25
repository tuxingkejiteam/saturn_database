DESC md5_uc;
ALTER TABLE  md5_uc ADD PRIMARY KEY(`md5`);
-- SELECT `md5` ,COUNT(`md5`) FROM md5_uc GROUP BY `md5`;
SELECT `md5`, `uc`, COUNT(`md5`) FROM md5_uc GROUP BY `uc` HAVING COUNT(`md5`) > 1;
SELECT `md5`,COUNT(`md5`) FROM md5_uc GROUP BY `md5` HAVING COUNT(`md5`) > 1;

-- 按条件删除表
DELETE FROM md5_uc WHERE `md5` IN(
	SELECT `md5` FROM(
		SELECT `md5` FROM md5_uc GROUP BY `md5`  HAVING COUNT(`md5`) > 1
		) AS tmp
);

	SELECT `md5` FROM(
		SELECT `md5` FROM md5_uc GROUP BY `md5` HAVING COUNT(`md5`) > 1
		) AS tmp


INSERT IGNORE INTO `目标标注表` VALUES ('asdfghj', 'cpb_ps', -1);
INSERT INTO `目标标注表` VALUES ('asdfghj', 'cpb_nor', -1) ON DUPLICATE KEY UPDATE 置信度=置信度+1;
INSERT INTO `目标标注表` VALUES ('asdfghj', 'cpb_nor', -1) ON DUPLICATE KEY UPDATE;
INSERT INTO `目标标注表` VALUES ('asdfghj', 'cpb_dirty', -1);

INSERT INTO `编码使用记录表` (`日期编码`) VALUES('Abc');\

INSERT IGNORE INTO `MD5对照表` VALUES('f341a333a4bb011aa8bf0f2fce395041', 'adsffgh');
SELECT UC FROM `MD5对照表` WHERE `MD5`='f97129f5e5e76f2ee7c53cfd1f4b9b8c';
TRUNCATE TABLE MD5对照表;

SELECT `唯一编码`,`标签`FROM `目标标注表` WHERE (`标签`='a' OR `标签`='b' OR `标签`='c') AND (置信度>1 OR 置信度<-1)
GROUP BY `唯一编码`  HAVING COUNT(`唯一编码`) = 3;

SELECT * FROM `目标标注表` WHERE `唯一编码`='Dnf001x' AND (`标签`='a' OR `标签`='b' OR `标签`='c');

INSERT INTO `目标标注表` VALUES('测试1','1',1);
INSERT INTO `目标标注表` VALUES('测试1','2',-1);
INSERT INTO `目标标注表` VALUES('测试2','2',1);
INSERT INTO `目标标注表` VALUES('测试2','3',-1);
INSERT INTO `目标标注表` VALUES('测试3','3',1);

INSERT INTO `编码使用记录表` (`日期编码`,`已使用数量`) VALUES ('abc',0)  ON DUPLICATE KEY UPDATE `已使用数量`=100; 
select `唯一编码` from `目标标注表` where `唯一编码` like 'Dni%' group by `唯一编码` HAVING COUNT(`唯一编码`) >= 1;
