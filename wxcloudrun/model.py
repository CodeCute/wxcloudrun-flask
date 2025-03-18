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
