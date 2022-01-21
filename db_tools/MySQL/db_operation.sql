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
