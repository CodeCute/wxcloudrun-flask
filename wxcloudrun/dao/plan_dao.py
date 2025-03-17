import logging
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.models.travel_plan import TravelPlan, TravelPlanItem

# 初始化日志
logger = logging.getLogger('log')


def create_travel_plan(plan):
    """
    创建行程计划
    :param plan: 行程计划实体
    :return: 创建的行程计划ID
    """
    try:
        db.session.add(plan)
        db.session.commit()
        return plan.id
    except OperationalError as e:
        logger.info("create_travel_plan errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_user_travel_plans(user_id):
    """
    获取用户行程计划列表
    :param user_id: 用户ID
    :return: 行程计划列表
    """
    try:
        return TravelPlan.query.filter(TravelPlan.user_id == user_id).order_by(TravelPlan.created_at.desc()).all()
    except OperationalError as e:
        logger.info("get_user_travel_plans errorMsg= {} ".format(e))
        return []


def get_travel_plan_by_id(plan_id):
    """
    根据ID获取行程计划详情
    :param plan_id: 行程计划ID
    :return: 行程计划实体
    """
    try:
        return TravelPlan.query.get(plan_id)
    except OperationalError as e:
        logger.info("get_travel_plan_by_id errorMsg= {} ".format(e))
        return None


def add_travel_plan_item(plan_item):
    """
    添加行程项目
    :param plan_item: 行程项目实体
    :return: 行程项目ID
    """
    try:
        db.session.add(plan_item)
        db.session.commit()
        return plan_item.id
    except OperationalError as e:
        logger.info("add_travel_plan_item errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def get_travel_plan_items(plan_id):
    """
    获取行程计划项目列表
    :param plan_id: 行程计划ID
    :return: 行程项目列表
    """
    try:
        return TravelPlanItem.query.filter(TravelPlanItem.plan_id == plan_id).order_by(TravelPlanItem.day, TravelPlanItem.id).all()
    except OperationalError as e:
        logger.info("get_travel_plan_items errorMsg= {} ".format(e))
        return [] 