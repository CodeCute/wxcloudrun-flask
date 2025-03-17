import logging
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.models.favorite import Favorite

# 初始化日志
logger = logging.getLogger('log')


def add_favorite(favorite):
    """
    添加收藏
    :param favorite: 收藏实体
    :return: 收藏ID
    """
    try:
        db.session.add(favorite)
        db.session.commit()
        return favorite.id
    except OperationalError as e:
        logger.info("add_favorite errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def remove_favorite(user_id, item_type, item_id):
    """
    取消收藏
    :param user_id: 用户ID
    :param item_type: 收藏类型
    :param item_id: 收藏项目ID
    """
    try:
        favorite = Favorite.query.filter(
            Favorite.user_id == user_id,
            Favorite.type == item_type,
            Favorite.item_id == item_id
        ).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
    except OperationalError as e:
        logger.info("remove_favorite errorMsg= {} ".format(e))
        db.session.rollback()


def get_user_favorites(user_id, item_type=None):
    """
    获取用户收藏列表
    :param user_id: 用户ID
    :param item_type: 收藏类型
    :return: 收藏列表
    """
    try:
        query = Favorite.query.filter(Favorite.user_id == user_id)
        if item_type:
            query = query.filter(Favorite.type == item_type)
        return query.order_by(Favorite.created_at.desc()).all()
    except OperationalError as e:
        logger.info("get_user_favorites errorMsg= {} ".format(e))
        return [] 