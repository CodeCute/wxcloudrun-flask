from datetime import datetime
from wxcloudrun import db

# 景点表
class Attraction(db.Model):
    __tablename__ = 'Attraction'
    
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