CREATE TABLE `user_info` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(127) NOT NULL DEFAULT '',
  `user_alias` varchar(127) NOT NULL DEFAULT '',
	`user_number` varchar(127) NOT NULL DEFAULT '',
	`user_type` tinyint(1) unsigned NOT NULL DEFAULT 0,
	`dept_id` bigint(20) unsigned NOT NULL DEFAULT 0,
  `password` varchar(127) NOT NULL DEFAULT '',
	`account_balance` bigint(20) unsigned NOT NULL DEFAULT 0,
	`disabled` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
	UNIQUE `uni_user_alias`(`user_alias`),
	UNIQUE `uni_user_number`(`user_number`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `gym` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `gym_name` varchar(127) NOT NULL DEFAULT '',
  `location` varchar(127) NOT NULL DEFAULT '',
	`manager_number` varchar(127) NOT NULL DEFAULT '',
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `department` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `dept_name` varchar(127) NOT NULL DEFAULT '',
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
	UNIQUE `uni_dept_name`(`dept_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `period_data` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `period_class_id` bigint(20) unsigned NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `court_resource` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `period_id` bigint(20) unsigned NOT NULL,
  `court_id` bigint(20) unsigned NOT NULL,
  `court_number` bigint(20) unsigned NOT NULL,
  `occupied` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `max_order_count` bigint(20) unsigned NOT NULL,
  `order_count` bigint(20) unsigned NOT NULL,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `schedule` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `court_id` bigint(20) unsigned NOT NULL,
  `date` datetime NOT NULL,
  `total` bigint(20) unsigned NOT NULL,
  `order_count` bigint(20) unsigned NOT NULL,
  `occupied_count` bigint(20) unsigned NOT NULL,
  `visible` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `enabled` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `create_time` datetime NOT NULL,
  `update_time` datetime NOT NULL,
  `record_status` tinyint(1) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
