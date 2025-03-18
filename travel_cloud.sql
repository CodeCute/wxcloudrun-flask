-- 创建travel_cloud数据库
CREATE DATABASE IF NOT EXISTS `flask_demo` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE `flask_demo`;

-- 创建计数表
CREATE TABLE IF NOT EXISTS `Counters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `count` int(11) NOT NULL DEFAULT 1,
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建用户信息表
CREATE TABLE IF NOT EXISTS `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `openid` varchar(100) NOT NULL COMMENT '微信用户唯一标识',
  `nickname` varchar(50) DEFAULT NULL COMMENT '用户昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像URL',
  `gender` int(11) DEFAULT 0 COMMENT '性别，0未知，1男，2女',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号码',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `openid` (`openid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建旅游指南表
CREATE TABLE IF NOT EXISTS `TravelGuide` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL COMMENT '指南标题',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图片URL',
  `description` text DEFAULT NULL COMMENT '指南简介',
  `content` text DEFAULT NULL COMMENT '指南内容',
  `author` varchar(50) DEFAULT NULL COMMENT '作者名称',
  `view_count` int(11) DEFAULT 0 COMMENT '浏览次数',
  `like_count` int(11) DEFAULT 0 COMMENT '点赞数',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建景点表
CREATE TABLE IF NOT EXISTS `Attraction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL COMMENT '景点名称',
  `cover_image` varchar(255) DEFAULT NULL COMMENT '封面图片URL',
  `images` text DEFAULT NULL COMMENT '图片URLs，JSON格式',
  `description` text DEFAULT NULL COMMENT '景点描述',
  `address` varchar(255) DEFAULT NULL COMMENT '地址',
  `location` varchar(100) DEFAULT NULL COMMENT '经纬度，格式为"纬度,经度"',
  `price` float DEFAULT NULL COMMENT '门票价格',
  `opening_hours` varchar(255) DEFAULT NULL COMMENT '开放时间',
  `tips` text DEFAULT NULL COMMENT '游玩提示',
  `category` varchar(50) DEFAULT NULL COMMENT '景点类别',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建收藏表
CREATE TABLE IF NOT EXISTS `Favorite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `type` varchar(20) NOT NULL COMMENT '收藏类型：guide或attraction',
  `item_id` int(11) NOT NULL COMMENT '收藏项目ID',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `favorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建行程计划表
CREATE TABLE IF NOT EXISTS `TravelPlan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL COMMENT '用户ID',
  `title` varchar(100) NOT NULL COMMENT '行程标题',
  `start_date` date DEFAULT NULL COMMENT '开始日期',
  `end_date` date DEFAULT NULL COMMENT '结束日期',
  `description` text DEFAULT NULL COMMENT '行程描述',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `travelplan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建行程项目表
CREATE TABLE IF NOT EXISTS `TravelPlanItem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plan_id` int(11) NOT NULL COMMENT '行程ID',
  `day` int(11) NOT NULL COMMENT '行程第几天',
  `attraction_id` int(11) DEFAULT NULL COMMENT '景点ID',
  `time_period` varchar(50) DEFAULT NULL COMMENT '时间段，如"上午"、"下午"等',
  `note` text DEFAULT NULL COMMENT '备注',
  `createdAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updatedAt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `plan_id` (`plan_id`),
  KEY `attraction_id` (`attraction_id`),
  CONSTRAINT `travelplanitem_ibfk_1` FOREIGN KEY (`plan_id`) REFERENCES `TravelPlan` (`id`) ON DELETE CASCADE,
  CONSTRAINT `travelplanitem_ibfk_2` FOREIGN KEY (`attraction_id`) REFERENCES `Attraction` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入示例数据 - 用户
INSERT INTO `User` (`openid`, `nickname`, `avatar`, `gender`, `phone`) VALUES
('admin', '管理员', 'https://example.com/images/admin.jpg', 1, '13800138000');

-- 插入示例数据 - 旅游指南
INSERT INTO `TravelGuide` (`title`, `cover_image`, `description`, `content`, `author`, `view_count`, `like_count`) VALUES
('北京三日游完美攻略', 'https://example.com/images/beijing.jpg', '北京三日游完美攻略，为您提供最佳旅游参考', '# 北京三日游完美攻略\n\n这是一篇详细的旅游攻略，内容包括景点、美食、交通等详细信息...\n\n## 推荐景点\n\n- 景点1\n- 景点2\n- 景点3\n\n## 美食推荐\n\n1. 特色美食1\n2. 特色美食2\n3. 特色美食3', '旅行达人', 500, 50),
('上海必去景点推荐', 'https://example.com/images/shanghai.jpg', '上海必去景点推荐，为您提供最佳旅游参考', '# 上海必去景点推荐\n\n这是一篇详细的旅游攻略，内容包括景点、美食、交通等详细信息...\n\n## 推荐景点\n\n- 景点1\n- 景点2\n- 景点3\n\n## 美食推荐\n\n1. 特色美食1\n2. 特色美食2\n3. 特色美食3', '旅行达人', 600, 60),
('成都美食之旅', 'https://example.com/images/chengdu.jpg', '成都美食之旅，为您提供最佳旅游参考', '# 成都美食之旅\n\n这是一篇详细的旅游攻略，内容包括景点、美食、交通等详细信息...\n\n## 推荐景点\n\n- 景点1\n- 景点2\n- 景点3\n\n## 美食推荐\n\n1. 特色美食1\n2. 特色美食2\n3. 特色美食3', '旅行达人', 700, 70),
('云南民族文化探索', 'https://example.com/images/yunnan.jpg', '云南民族文化探索，为您提供最佳旅游参考', '# 云南民族文化探索\n\n这是一篇详细的旅游攻略，内容包括景点、美食、交通等详细信息...\n\n## 推荐景点\n\n- 景点1\n- 景点2\n- 景点3\n\n## 美食推荐\n\n1. 特色美食1\n2. 特色美食2\n3. 特色美食3', '旅行达人', 800, 80),
('西安历史古迹一日游', 'https://example.com/images/xian.jpg', '西安历史古迹一日游，为您提供最佳旅游参考', '# 西安历史古迹一日游\n\n这是一篇详细的旅游攻略，内容包括景点、美食、交通等详细信息...\n\n## 推荐景点\n\n- 景点1\n- 景点2\n- 景点3\n\n## 美食推荐\n\n1. 特色美食1\n2. 特色美食2\n3. 特色美食3', '旅行达人', 900, 90);

-- 插入示例数据 - 景点
INSERT INTO `Attraction` (`name`, `cover_image`, `images`, `description`, `address`, `location`, `price`, `opening_hours`, `tips`, `category`) VALUES
('故宫博物院', 'https://example.com/images/forbidden_city.jpg', '[\"https://example.com/images/forbidden_city.jpg\",\"https://example.com/images/great_wall.jpg\",\"https://example.com/images/west_lake.jpg\"]', '故宫博物院是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区故宫博物院景区', '30.5,100.8', 60, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '文化古迹'),
('长城', 'https://example.com/images/great_wall.jpg', '[\"https://example.com/images/great_wall.jpg\",\"https://example.com/images/west_lake.jpg\",\"https://example.com/images/huangshan.jpg\"]', '长城是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区长城景区', '31.0,101.6', 40, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '文化古迹'),
('西湖', 'https://example.com/images/west_lake.jpg', '[\"https://example.com/images/west_lake.jpg\",\"https://example.com/images/huangshan.jpg\",\"https://example.com/images/jiuzhaigou.jpg\"]', '西湖是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区西湖景区', '31.5,102.4', 100, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '自然风光'),
('黄山', 'https://example.com/images/huangshan.jpg', '[\"https://example.com/images/huangshan.jpg\",\"https://example.com/images/jiuzhaigou.jpg\",\"https://example.com/images/zhangjiajie.jpg\"]', '黄山是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区黄山景区', '32.0,103.2', 120, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '自然风光'),
('九寨沟', 'https://example.com/images/jiuzhaigou.jpg', '[\"https://example.com/images/jiuzhaigou.jpg\",\"https://example.com/images/zhangjiajie.jpg\",\"https://example.com/images/gulangyu.jpg\"]', '九寨沟是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区九寨沟景区', '32.5,104.0', 80, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '自然风光'),
('张家界', 'https://example.com/images/zhangjiajie.jpg', '[\"https://example.com/images/zhangjiajie.jpg\",\"https://example.com/images/gulangyu.jpg\",\"https://example.com/images/lijiang.jpg\"]', '张家界是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区张家界景区', '33.0,104.8', 140, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '自然风光'),
('鼓浪屿', 'https://example.com/images/gulangyu.jpg', '[\"https://example.com/images/gulangyu.jpg\",\"https://example.com/images/lijiang.jpg\",\"https://example.com/images/forbidden_city.jpg\"]', '鼓浪屿是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区鼓浪屿景区', '33.5,105.6', 90, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '文化古迹'),
('丽江古城', 'https://example.com/images/lijiang.jpg', '[\"https://example.com/images/lijiang.jpg\",\"https://example.com/images/forbidden_city.jpg\",\"https://example.com/images/great_wall.jpg\"]', '丽江古城是中国著名的旅游景点，每年吸引大量游客前来观光。', '中国某省某市某区丽江古城景区', '34.0,106.4', 130, '08:00-17:00', '建议游玩时间：3小时，旺季人流量大，建议提前购票。', '文化古迹');

-- 插入示例数据 - 行程计划
INSERT INTO `TravelPlan` (`user_id`, `title`, `start_date`, `end_date`, `description`) VALUES
(1, '北京文化之旅', CURDATE(), CURDATE(), '探索北京的历史文化景点');

-- 插入示例数据 - 收藏
INSERT INTO `Favorite` (`user_id`, `type`, `item_id`) VALUES
(1, 'attraction', 1),
(1, 'guide', 1); 