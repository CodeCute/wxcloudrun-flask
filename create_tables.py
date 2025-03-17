#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wxcloudrun import db
from wxcloudrun.model import Counters, User, TravelGuide, Attraction, Favorite, TravelPlan, TravelPlanItem

def create_tables():
    """
    创建数据库表
    """
    db.create_all()
    print("数据库表创建成功")

if __name__ == '__main__':
    create_tables() 