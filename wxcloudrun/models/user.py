from datetime import datetime
from wxcloudrun import db

# 用户信息表
class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    openid = db.Column(db.String(100), unique=True, nullable=False, comment='微信用户唯一标识')
    nickname = db.Column(db.String(50), comment='用户昵称')
    avatar = db.Column(db.String(255), comment='头像URL')
    gender = db.Column(db.Integer, default=0, comment='性别，0未知，1男，2女')
    phone = db.Column(db.String(20), comment='手机号码')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now()) 