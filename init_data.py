#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from datetime import datetime
from wxcloudrun import app, db
from wxcloudrun.model import User, TravelGuide, Attraction, Favorite, TravelPlan, TravelPlanItem
from wxcloudrun.dao import create_user, create_travel_guide, create_attraction

def init_data():
    """
    初始化示例数据
    """
    with app.app_context():
        try:
            # 创建示例用户
            admin_user = User()
            admin_user.openid = 'admin'
            admin_user.nickname = '管理员'
            admin_user.avatar = 'https://example.com/images/admin.jpg'
            admin_user.gender = 1
            admin_user.phone = '13800138000'
            admin_id = create_user(admin_user)
            
            print(f"创建管理员用户成功，ID: {admin_id}")
            
            # 初始化旅游指南数据
            guide_titles = [
                "北京三日游完美攻略", 
                "上海必去景点推荐", 
                "成都美食之旅", 
                "云南民族文化探索", 
                "西安历史古迹一日游"
            ]
            guide_images = [
                "https://example.com/images/beijing.jpg",
                "https://example.com/images/shanghai.jpg",
                "https://example.com/images/chengdu.jpg",
                "https://example.com/images/yunnan.jpg",
                "https://example.com/images/xian.jpg"
            ]
            
            for i in range(5):
                guide = TravelGuide()
                guide.title = guide_titles[i]
                guide.cover_image = guide_images[i]
                guide.description = f"{guide_titles[i]}，为您提供最佳旅游参考"
                guide.content = f"# {guide_titles[i]}\n\n这是一篇详细的旅游攻略，内容包括景点、美食、交通等详细信息...\n\n## 推荐景点\n\n- 景点1\n- 景点2\n- 景点3\n\n## 美食推荐\n\n1. 特色美食1\n2. 特色美食2\n3. 特色美食3"
                guide.author = "旅行达人"
                guide.view_count = random.randint(100, 1000)
                guide.like_count = random.randint(10, 100)
                guide_id = create_travel_guide(guide)
                print(f"创建旅游指南成功，ID: {guide_id}, 标题: {guide.title}")
            
            # 初始化景点数据
            attraction_names = [
                "故宫博物院", 
                "长城", 
                "西湖", 
                "黄山", 
                "九寨沟",
                "张家界", 
                "鼓浪屿", 
                "丽江古城"
            ]
            attraction_images = [
                "https://example.com/images/forbidden_city.jpg",
                "https://example.com/images/great_wall.jpg",
                "https://example.com/images/west_lake.jpg",
                "https://example.com/images/huangshan.jpg",
                "https://example.com/images/jiuzhaigou.jpg",
                "https://example.com/images/zhangjiajie.jpg",
                "https://example.com/images/gulangyu.jpg",
                "https://example.com/images/lijiang.jpg"
            ]
            attraction_categories = ["文化古迹", "自然风光", "自然风光", "自然风光", "自然风光", "自然风光", "文化古迹", "文化古迹"]
            
            for i in range(8):
                attraction = Attraction()
                attraction.name = attraction_names[i]
                attraction.cover_image = attraction_images[i]
                images = [attraction_images[i], attraction_images[(i+1)%8], attraction_images[(i+2)%8]]
                attraction.images = json.dumps(images)
                attraction.description = f"{attraction_names[i]}是中国著名的旅游景点，每年吸引大量游客前来观光。"
                attraction.address = f"中国某省某市某区{attraction_names[i]}景区"
                attraction.location = f"{30 + i * 0.5},{100 + i * 0.8}"
                attraction.price = random.randint(5, 30) * 10
                attraction.opening_hours = "08:00-17:00"
                attraction.tips = "建议游玩时间：3小时，旺季人流量大，建议提前购票。"
                attraction.category = attraction_categories[i]
                attraction_id = create_attraction(attraction)
                print(f"创建景点成功，ID: {attraction_id}, 名称: {attraction.name}")
            
            # 为管理员创建示例行程
            plan = TravelPlan()
            plan.user_id = admin_id
            plan.title = "北京文化之旅"
            plan.start_date = datetime.now().date()
            plan.end_date = datetime.now().date()
            plan.description = "探索北京的历史文化景点"
            db.session.add(plan)
            db.session.commit()
            
            print(f"创建行程计划成功，ID: {plan.id}, 标题: {plan.title}")
            
            # 添加收藏
            favorite = Favorite()
            favorite.user_id = admin_id
            favorite.type = "attraction"
            favorite.item_id = 1  # 收藏第一个景点
            db.session.add(favorite)
            
            favorite2 = Favorite()
            favorite2.user_id = admin_id
            favorite2.type = "guide"
            favorite2.item_id = 1  # 收藏第一个旅游指南
            db.session.add(favorite2)
            db.session.commit()
            
            print("添加收藏成功")
            
            print("示例数据初始化完成")
            
        except Exception as e:
            print(f"初始化数据出错: {str(e)}")

if __name__ == '__main__':
    init_data() 