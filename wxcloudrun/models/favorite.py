from datetime import datetime
from wxcloudrun import db

# 收藏表
class Favorite(db.Model):
    __tablename__ = 'Favorite'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, comment='用户ID')
    type = db.Column(db.String(20), nullable=False, comment='收藏类型：guide或attraction')
    item_id = db.Column(db.Integer, nullable=False, comment='收藏项目ID')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now()) 