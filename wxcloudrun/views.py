from datetime import datetime
import json
import os
import sys
import uuid
import logging
import random
from flask import render_template, request, g
from wxcloudrun import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.dao import get_user_by_openid, create_user, update_user
from wxcloudrun.dao import get_travel_guides, get_travel_guide_by_id, create_travel_guide
from wxcloudrun.dao import get_attractions, get_attraction_by_id, create_attraction
from wxcloudrun.dao import add_favorite, remove_favorite, get_user_favorites
from wxcloudrun.dao import create_travel_plan, get_user_travel_plans, get_travel_plan_by_id, add_travel_plan_item, get_travel_plan_items
from wxcloudrun.model import Counters, User, TravelGuide, Attraction, Favorite, TravelPlan, TravelPlanItem
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')

# 注意：其他API路由已经在各自的模块文件中定义
# counter.py - 计数器相关路由
# user.py - 用户相关路由
# guide.py - 旅游指南相关路由
# attraction.py - 景点相关路由
# favorite.py - 收藏相关路由
# plan.py - 行程计划相关路由
# initialize.py - 数据初始化相关路由
