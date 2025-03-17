from datetime import datetime
from wxcloudrun import db

# 旅游指南表
class TravelGuide(db.Model):
    __tablename__ = 'TravelGuide'
    
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