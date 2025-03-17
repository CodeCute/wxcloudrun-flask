from datetime import datetime
from wxcloudrun import db

# 行程计划表
class TravelPlan(db.Model):
    __tablename__ = 'TravelPlan'
    
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
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('TravelPlan.id'), nullable=False, comment='行程ID')
    day = db.Column(db.Integer, nullable=False, comment='行程第几天')
    attraction_id = db.Column(db.Integer, db.ForeignKey('Attraction.id'), comment='景点ID')
    time_period = db.Column(db.String(50), comment='时间段，如"上午"、"下午"等')
    note = db.Column(db.Text, comment='备注')
    created_at = db.Column('createdAt', db.TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = db.Column('updatedAt', db.TIMESTAMP, nullable=False, default=datetime.now()) 