import logging
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.models.travel_guide import TravelGuide

# 初始化日志
logger = logging.getLogger('log')


def get_travel_guides(page=1, page_size=10):
    """
    获取旅游指南列表
    :param page: 页码
    :param page_size: 每页数量
    :return: 旅游指南列表
    """
    try:
        offset = (page - 1) * page_size
        return TravelGuide.query.order_by(TravelGuide.created_at.desc()).offset(offset).limit(page_size).all()
    except OperationalError as e:
        logger.info("get_travel_guides errorMsg= {} ".format(e))
        return []


def get_travel_guide_by_id(guide_id):
    """
    根据ID获取旅游指南详情
    :param guide_id: 旅游指南ID
    :return: 旅游指南实体
    """
    try:
        guide = TravelGuide.query.get(guide_id)
        if guide:
            # 更新浏览次数
            guide.view_count += 1
            db.session.commit()
        return guide
    except OperationalError as e:
        logger.info("get_travel_guide_by_id errorMsg= {} ".format(e))
        return None


def create_travel_guide(guide):
    """
    创建旅游指南
    :param guide: 旅游指南实体
    :return: 创建的旅游指南ID
    """
    try:
        db.session.add(guide)
        db.session.commit()
        return guide.id
    except OperationalError as e:
        logger.info("create_travel_guide errorMsg= {} ".format(e))
        db.session.rollback()
        return None 