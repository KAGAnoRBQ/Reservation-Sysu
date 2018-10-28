# Reservation-Sysu

关于数据库的设计
1. 主键统一叫 id 不要加前缀
2. 增加一个部门表？
3. id统一用bigint 不要使用bool 用tinyint 你以为真存一个位？ 后期加属性的时候 只有true和false很尴尬
4. gym表的 manager字段改为manager_id（user_id）吧 用manager算什么嘛 名字？重名咋整？

按照一下的sql来规范建表吧：

CREATE TABLE `user_info` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,<br>
  `user_name` varchar(255) NOT NULL DEFAULT '',<br>
  `user_alias` varchar(255) NOT NULL DEFAULT '',
	`user_number` varchar(255) NOT NULL DEFAULT '',
	`user_type` tinyint(1) unsigned NOT NULL DEFAULT 0,
	`dept_id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `password` varchar(255) NOT NULL DEFAULT '',
	`account_balance` bigint(20) unsigned NOT NULL DEFAULT 0,
	`disabled` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
	UNIQUE `uni_username`(`user_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

关于 API 接口
参照 first_group_api.docx 来写吧
