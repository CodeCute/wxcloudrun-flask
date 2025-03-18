from datetime import datetime

from wxcloudrun import db


# 计数表
class Counters(db.Model):
    # 设置结构体表格名称
    __tablename__ = 'Counters'
    # 允许表重新定义
    __table_args__ = {'extend_existing': True}

    # 设定结构体对应表格的字段
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=1)
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 用户信息表
class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(100), unique=True, nullable=False, comment='微信用户唯一标识')
    nickname = db.Column(db.String(50), comment='用户昵称')
    avatar = db.Column(db.String(255), comment='头像URL')
    gender = db.Column(db.Integer, default=0, comment='性别，0未知，1男，2女')
    phone = db.Column(db.String(20), comment='手机号码')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 旅游指南表
class TravelGuide(db.Model):
    __tablename__ = 'TravelGuide'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, comment='指南标题')
    cover_image = db.Column(db.String(255), comment='封面图片URL')
    description = db.Column(db.Text, comment='指南简介')
    content = db.Column(db.Text, comment='指南内容')
    author = db.Column(db.String(50), comment='作者名称')
    view_count = db.Column(db.Integer, default=0, comment='浏览次数')
    like_count = db.Column(db.Integer, default=0, comment='点赞数')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 景点表
class Attraction(db.Model):
    __tablename__ = 'Attraction'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, comment='景点名称')
    cover_image = db.Column(db.String(255), comment='封面图片URL')
    images = db.Column(db.Text, comment='图片URLs，JSON格式')
    description = db.Column(db.Text, comment='景点描述')
    address = db.Column(db.String(255), comment='地址')
    location = db.Column(db.String(100), comment='经纬度，格式为"纬度,经度"')
    price = db.Column(db.Float, comment='门票价格')
    opening_hours = db.Column(db.String(255), comment='开放时间')
    tips = db.Column(db.Text, comment='游玩提示')
    category = db.Column(db.String(50), comment='景点类别')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 收藏表
class Favorite(db.Model):
    __tablename__ = 'Favorite'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='用户ID')
    type = db.Column(db.String(20), nullable=False, comment='收藏类型：guide或attraction')
    item_id = db.Column(db.Integer, nullable=False, comment='收藏项目ID')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 行程计划表
class TravelPlan(db.Model):
    __tablename__ = 'TravelPlan'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='用户ID')
    title = db.Column(db.String(100), nullable=False, comment='行程标题')
    start_date = db.Column(db.Date, comment='开始日期')
    end_date = db.Column(db.Date, comment='结束日期')
    description = db.Column(db.Text, comment='行程描述')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 行程项目表
class TravelPlanItem(db.Model):
    __tablename__ = 'TravelPlanItem'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('TravelPlan.id'), nullable=False, comment='行程ID')
    day = db.Column(db.Integer, nullable=False, comment='行程第几天')
    attraction_id = db.Column(db.Integer, db.ForeignKey('Attraction.id'), comment='景点ID')
    time_period = db.Column(db.String(50), comment='时间段，如"上午"、"下午"等')
    note = db.Column(db.Text, comment='备注')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now())


# 资讯/动态表
class News(db.Model):
    __tablename__ = 'news'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment='资讯标题')
    content = db.Column(db.Text, nullable=False, comment='资讯内容')
    cover_image = db.Column(db.String(255), comment='封面图片URL')
    author_id = db.Column(db.String(50), nullable=False, comment='作者ID')
    view_count = db.Column(db.Integer, default=0, comment='浏览次数')
    like_count = db.Column(db.Integer, default=0, comment='点赞数')
    comment_count = db.Column(db.Integer, default=0, comment='评论数')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())


# 资讯点赞表
class NewsLike(db.Model):
    __tablename__ = 'news_likes'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, comment='用户ID')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    # 添加唯一约束
    __table_args__ = (
        db.UniqueConstraint('news_id', 'user_id', name='uq_news_like'),
        {'extend_existing': True}
    )


# 资讯评论表
class NewsComment(db.Model):
    __tablename__ = 'news_comments'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, comment='评论用户ID')
    content = db.Column(db.Text, nullable=False, comment='评论内容')
    parent_id = db.Column(db.Integer, db.ForeignKey('news_comments.id', ondelete='SET NULL'), comment='父评论ID')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())


# 向导标签表
class CompanionTag(db.Model):
    __tablename__ = 'companion_tags'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, comment='标签名称')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())


# 向导表
class Companion(db.Model):
    __tablename__ = 'companions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False, comment='用户ID')
    title = db.Column(db.String(255), nullable=False, comment='向导标题')
    description = db.Column(db.Text, comment='向导描述')
    avatar = db.Column(db.String(255), comment='头像URL')
    cover_image = db.Column(db.String(255), comment='封面图片URL')
    price = db.Column(db.DECIMAL(10, 2), nullable=False, comment='价格')
    location = db.Column(db.String(100), nullable=False, comment='地点')
    experience_years = db.Column(db.Integer, default=0, comment='经验年数')
    languages = db.Column(db.String(255), comment='语言能力')
    rating = db.Column(db.DECIMAL(3, 2), default=5.00, comment='评分')
    review_count = db.Column(db.Integer, default=0, comment='评价数量')
    status = db.Column(db.TINYINT, default=1, comment='状态：1活跃，0非活跃')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())


# 向导标签关系表
class CompanionTagRelation(db.Model):
    __tablename__ = 'companion_tag_relations'
    __table_args__ = {'extend_existing': True}
    
    companion_id = db.Column(db.Integer, db.ForeignKey('companions.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('companion_tags.id', ondelete='CASCADE'), primary_key=True)


# 向导预约表
class CompanionReservation(db.Model):
    __tablename__ = 'companion_reservations'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companion_id = db.Column(db.Integer, db.ForeignKey('companions.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, comment='用户ID')
    start_date = db.Column(db.Date, nullable=False, comment='开始日期')
    end_date = db.Column(db.Date, nullable=False, comment='结束日期')
    traveler_count = db.Column(db.Integer, nullable=False, default=1, comment='旅行人数')
    special_needs = db.Column(db.Text, comment='特殊需求')
    status = db.Column(db.TINYINT, default=0, comment='状态：0待确认，1已确认，2已完成，3已取消')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())


# 向导评价表
class CompanionReview(db.Model):
    __tablename__ = 'companion_reviews'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('companion_reservations.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, comment='用户ID')
    companion_id = db.Column(db.Integer, db.ForeignKey('companions.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.DECIMAL(3, 2), nullable=False, comment='评分')
    content = db.Column(db.Text, comment='评价内容')
    images = db.Column(db.Text, comment='图片URLs，逗号分隔')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())


# 用户关注表
class UserFollow(db.Model):
    __tablename__ = 'user_follows'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.String(50), nullable=False, comment='关注者ID')
    following_id = db.Column(db.String(50), nullable=False, comment='被关注者ID')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    
    # 添加唯一约束
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'following_id', name='uq_user_follow'),
        {'extend_existing': True}
    )


# 旅行解决方案表
class Solution(db.Model):
    __tablename__ = 'solutions'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, comment='解决方案标题')
    description = db.Column(db.Text, comment='解决方案描述')
    cover_image = db.Column(db.String(255), comment='封面图片URL')
    content = db.Column(db.Text, nullable=False, comment='解决方案内容')
    duration = db.Column(db.Integer, comment='天数')
    price_estimate = db.Column(db.DECIMAL(10, 2), comment='估算价格')
    difficulty = db.Column(db.TINYINT, default=1, comment='难度：1-5，5为最难')
    view_count = db.Column(db.Integer, default=0, comment='浏览次数')
    apply_count = db.Column(db.Integer, default=0, comment='应用次数')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())


# 解决方案应用表
class SolutionApplication(db.Model):
    __tablename__ = 'solution_applications'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    solution_id = db.Column(db.Integer, db.ForeignKey('solutions.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, comment='用户ID')
    travel_date = db.Column(db.Date, comment='旅行日期')
    notes = db.Column(db.Text, comment='备注')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())


# 反馈表
class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False, comment='用户ID')
    type = db.Column(db.String(50), nullable=False, comment='反馈类型')
    content = db.Column(db.Text, nullable=False, comment='反馈内容')
    contact = db.Column(db.String(100), comment='联系方式')
    images = db.Column(db.Text, comment='图片URLs，逗号分隔')
    status = db.Column(db.TINYINT, default=0, comment='状态：0未处理，1处理中，2已处理')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())


# 关于我们信息表
class AboutInfo(db.Model):
    __tablename__ = 'about_info'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, comment='标题')
    content = db.Column(db.Text, nullable=False, comment='内容')
    type = db.Column(db.String(50), nullable=False, comment='类型：company, contact, agreement, privacy等')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.now(), onupdate=datetime.now())
