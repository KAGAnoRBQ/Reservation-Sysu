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

DROP TABLE IF EXISTS `court_order`;
CREATE TABLE `court_order`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `order_time` datetime(0) NOT NULL,
  `resource_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `pay_time` datetime(0) NOT NULL,
  `amount` int(16) UNSIGNED NOT NULL DEFAULT 0,
  `is_acked` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `ack_time` datetime(0) NOT NULL,
  `is_canceled` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `cancel_time` datetime(0) NOT NULL,
  `is_used` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `update_time` datetime(0) NULL ON UPDATE CURRENT_TIMESTAMP(0),
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4;

DROP TABLE IF EXISTS `account`;
CREATE TABLE `account`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `order_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `account_summary` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `account_time` datetime(0) NOT NULL,
  `amount` int(16) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4;

DROP TABLE IF EXISTS `court`;
CREATE TABLE `court`  (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `gym_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `court_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `court_type` tinyint(16) UNSIGNED NOT NULL DEFAULT 0,
  `court_count` int(16) UNSIGNED NOT NULL DEFAULT 0,
  `max_order_count` int(16) UNSIGNED NOT NULL DEFAULT 1,
  `court_fee` int(16) UNSIGNED NOT NULL DEFAULT 0,
  `order_days` int(16) UNSIGNED NOT NULL DEFAULT 0,
  `period_class_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4;

