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


-- 资讯/动态相关表
CREATE TABLE IF NOT EXISTS news (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    cover_image VARCHAR(255),
    author_id VARCHAR(50) NOT NULL,
    view_count INT DEFAULT 0,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news_likes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    news_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (news_id, user_id),
    FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS news_comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    news_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    parent_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (news_id) REFERENCES news(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES news_comments(id) ON DELETE SET NULL
);

-- 结伴旅行相关表
CREATE TABLE IF NOT EXISTS companion_tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS companions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    avatar VARCHAR(255),
    cover_image VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    location VARCHAR(100) NOT NULL,
    experience_years INT DEFAULT 0,
    languages VARCHAR(255),
    rating DECIMAL(3, 2) DEFAULT 5.00,
    review_count INT DEFAULT 0,
    status TINYINT DEFAULT 1 COMMENT '1: 活跃, 0: 非活跃',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS companion_tag_relations (
    companion_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (companion_id, tag_id),
    FOREIGN KEY (companion_id) REFERENCES companions(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES companion_tags(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS companion_reservations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    companion_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    traveler_count INT NOT NULL DEFAULT 1,
    special_needs TEXT,
    status TINYINT DEFAULT 0 COMMENT '0: 待确认, 1: 已确认, 2: 已完成, 3: 已取消',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (companion_id) REFERENCES companions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS companion_reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    companion_id INT NOT NULL,
    rating DECIMAL(3, 2) NOT NULL,
    content TEXT,
    images TEXT COMMENT '逗号分隔的图片URL',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES companion_reservations(id) ON DELETE CASCADE,
    FOREIGN KEY (companion_id) REFERENCES companions(id) ON DELETE CASCADE
);

-- 用户互动相关表
CREATE TABLE IF NOT EXISTS user_follows (
    id INT PRIMARY KEY AUTO_INCREMENT,
    follower_id VARCHAR(50) NOT NULL COMMENT '关注者ID',
    following_id VARCHAR(50) NOT NULL COMMENT '被关注者ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY (follower_id, following_id)
);

-- 解决方案相关表
CREATE TABLE IF NOT EXISTS solutions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    cover_image VARCHAR(255),
    content TEXT NOT NULL,
    duration INT COMMENT '天数',
    price_estimate DECIMAL(10, 2),
    difficulty TINYINT DEFAULT 1 COMMENT '1-5, 5为最难',
    view_count INT DEFAULT 0,
    apply_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS solution_applications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    solution_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    travel_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (solution_id) REFERENCES solutions(id) ON DELETE CASCADE
);

-- 反馈相关表
CREATE TABLE IF NOT EXISTS feedbacks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50) NOT NULL,
    type VARCHAR(50) NOT NULL COMMENT '反馈类型',
    content TEXT NOT NULL,
    contact VARCHAR(100),
    images TEXT COMMENT '逗号分隔的图片URL',
    status TINYINT DEFAULT 0 COMMENT '0: 未处理, 1: 处理中, 2: 已处理',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS about_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    type VARCHAR(50) NOT NULL COMMENT '关于我们类型: company, contact, agreement, privacy等',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入测试数据
-- 资讯测试数据
INSERT INTO news (title, content, cover_image, author_id, view_count, like_count, comment_count) VALUES
('日本樱花季旅游指南', '日本樱花季通常在3月下旬到4月上旬，本文为您提供详细的赏樱攻略...', 'https://example.com/images/japan-sakura.jpg', 'user123', 1520, 89, 23),
('探秘云南古镇', '云南丽江、大理等古镇的深度游玩攻略，带您体验不一样的云南风情...', 'https://example.com/images/yunnan.jpg', 'user456', 982, 67, 15),
('欧洲自由行省钱技巧', '如何在欧洲自由行中省钱的实用技巧，包括交通、住宿、餐饮等各方面...', 'https://example.com/images/europe-travel.jpg', 'user789', 2341, 156, 42);

-- 点赞测试数据
INSERT INTO news_likes (news_id, user_id) VALUES
(1, 'user001'), (1, 'user002'), (1, 'user003'),
(2, 'user001'), (2, 'user004'),
(3, 'user002'), (3, 'user003'), (3, 'user005');

-- 评论测试数据
INSERT INTO news_comments (news_id, user_id, content, parent_id) VALUES
(1, 'user001', '去年去日本看樱花，真的太美了！', NULL),
(1, 'user002', '请问3月中旬去合适吗？', NULL),
(1, 'user003', '建议4月初去东京，樱花盛开的时候', 2),
(2, 'user004', '大理古城值得一去，环境很不错', NULL),
(3, 'user005', '欧洲交通卡真的很划算，强烈推荐', NULL);

-- 向导标签测试数据
INSERT INTO companion_tags (name) VALUES
('摄影'), ('徒步'), ('美食'), ('历史'), ('自驾'), ('购物'), ('潜水'), ('登山');

-- 向导测试数据
INSERT INTO companions (user_id, title, description, avatar, cover_image, price, location, experience_years, languages, rating, review_count) VALUES
('guide001', '巴厘岛专业向导', '5年巴厘岛带团经验，精通各种小众景点和体验', 'https://example.com/avatars/guide1.jpg', 'https://example.com/covers/bali.jpg', 800.00, '巴厘岛', 5, '中文,英文,印尼语', 4.92, 68),
('guide002', '京都深度游向导', '京都本地人，带您体验最地道的京都文化', 'https://example.com/avatars/guide2.jpg', 'https://example.com/covers/kyoto.jpg', 1200.00, '京都', 8, '中文,日语,英文', 4.88, 126),
('guide003', '巴黎艺术之旅', '艺术专业毕业，对巴黎各大博物馆了如指掌', 'https://example.com/avatars/guide3.jpg', 'https://example.com/covers/paris.jpg', 1500.00, '巴黎', 6, '中文,法语,英文', 4.95, 87);

-- 向导标签关系测试数据
INSERT INTO companion_tag_relations (companion_id, tag_id) VALUES
(1, 1), (1, 3), (1, 7),
(2, 2), (2, 4), (2, 3),
(3, 1), (3, 4), (3, 6);

-- 向导预约测试数据
INSERT INTO companion_reservations (companion_id, user_id, start_date, end_date, traveler_count, special_needs, status) VALUES
(1, 'user001', '2023-07-15', '2023-07-18', 2, '希望包含美食体验和摄影指导', 2),
(2, 'user002', '2023-08-10', '2023-08-12', 4, '有老人同行，需要行程轻松些', 1),
(3, 'user003', '2023-09-05', '2023-09-07', 1, '主要参观卢浮宫和奥赛博物馆', 0);

-- 向导评价测试数据
INSERT INTO companion_reviews (reservation_id, user_id, companion_id, rating, content, images) VALUES
(1, 'user001', 1, 5.00, '非常专业的向导，知识丰富，带我们去了很多小众的地方，拍了很多美照！', 'https://example.com/reviews/r1_1.jpg,https://example.com/reviews/r1_2.jpg'),
(2, 'user002', 2, 4.50, '行程安排得很合理，照顾到老人的需求，京都的历史文化讲解得很到位', NULL);

-- 用户关注测试数据
INSERT INTO user_follows (follower_id, following_id) VALUES
('user001', 'guide001'), ('user001', 'user002'),
('user002', 'guide002'), ('user003', 'guide001'),
('user004', 'guide003'), ('user005', 'user001');

-- 解决方案测试数据
INSERT INTO solutions (title, description, cover_image, content, duration, price_estimate, difficulty, view_count, apply_count) VALUES
('日本关西7日深度游', '大阪、京都、奈良经典行程，体验关西文化与美食', 'https://example.com/solutions/kansai.jpg', '详细的7日行程安排，包含交通、住宿、景点推荐...', 7, 12000.00, 2, 3245, 78),
('泰国清迈轻松3日游', '适合短期休假，体验清迈文化与美食的最佳路线', 'https://example.com/solutions/chiangmai.jpg', '3天2晚行程安排，包含寺庙游览、夜市体验、泰式按摩...', 3, 5000.00, 1, 2189, 103),
('新西兰南岛自驾8日', '新西兰南岛最经典的自驾路线，饱览壮丽自然风光', 'https://example.com/solutions/newzealand.jpg', '8天自驾路线，包含皇后镇、米尔福德峡湾、库克山等地...', 8, 25000.00, 4, 1876, 42);

-- 解决方案应用测试数据
INSERT INTO solution_applications (solution_id, user_id, travel_date, notes) VALUES
(1, 'user001', '2023-10-01', '计划十一假期出行，希望能提供更详细的住宿建议'),
(2, 'user003', '2023-08-15', '有没有推荐的特色餐厅？'),
(1, 'user004', '2023-09-20', NULL);

-- 反馈测试数据
INSERT INTO feedbacks (user_id, type, content, contact, images, status) VALUES
('user001', '功能建议', '希望能增加行程共享功能，方便和朋友一起规划旅行', 'user001@example.com', NULL, 1),
('user002', '问题反馈', '预约向导时遇到支付问题，无法完成支付', 'user002@example.com', 'https://example.com/feedback/fb1.jpg', 2),
('user003', '内容纠错', '日本关西攻略中京都岚山的营业时间有误', NULL, NULL, 0);

-- 关于我们信息测试数据
INSERT INTO about_info (title, content, type) VALUES
('旅行云简介', '旅行云是一家专注于为用户提供个性化旅行服务的平台...', 'company'),
('联系我们', '客服电话：400-123-4567\n邮箱：support@travelcloud.com', 'contact'),
('用户协议', '欢迎使用旅行云服务！本协议是您与旅行云之间关于使用旅行云服务的条款...', 'agreement'),
('隐私政策', '本隐私政策描述了我们如何收集、使用和处理您的个人信息...', 'privacy');
