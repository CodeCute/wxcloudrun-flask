import logging
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.models.attraction import Attraction

# 初始化日志
logger = logging.getLogger('log')


def get_attractions(page=1, page_size=10, category=None):
    """
    获取景点列表
    :param page: 页码
    :param page_size: 每页数量
    :param category: 景点类别
    :return: 景点列表
    """
    try:
        offset = (page - 1) * page_size
        query = Attraction.query
        if category:
            query = query.filter(Attraction.category == category)
        return query.order_by(Attraction.created_at.desc()).offset(offset).limit(page_size).all()
    except OperationalError as e:
        logger.info("get_attractions errorMsg= {} ".format(e))
        return []


def get_attraction_by_id(attraction_id):
    """
    根据ID获取景点详情
    :param attraction_id: 景点ID
    :return: 景点实体
    """
    try:
        return Attraction.query.get(attraction_id)
    except OperationalError as e:
        logger.info("get_attraction_by_id errorMsg= {} ".format(e))
        return None


def create_attraction(attraction):
    """
    创建景点
    :param attraction: 景点实体
    :return: 创建的景点ID
    """
    try:
        db.session.add(attraction)
        db.session.commit()
        return attraction.id
    except OperationalError as e:
        logger.info("create_attraction errorMsg= {} ".format(e))
        db.session.rollback()
        return None 