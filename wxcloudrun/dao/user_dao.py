import logging
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.models.user import User

# 初始化日志
logger = logging.getLogger('log')


def get_user_by_openid(openid):
    """
    根据微信openid获取用户信息
    :param openid: 微信用户唯一标识
    :return: 用户实体
    """
    try:
        return User.query.filter(User.openid == openid).first()
    except OperationalError as e:
        logger.info("get_user_by_openid errorMsg= {} ".format(e))
        return None


def create_user(user):
    """
    创建用户
    :param user: 用户实体
    :return: 创建的用户ID
    """
    try:
        db.session.add(user)
        db.session.commit()
        return user.id
    except OperationalError as e:
        logger.info("create_user errorMsg= {} ".format(e))
        db.session.rollback()
        return None


def update_user(user):
    """
    更新用户信息
    :param user: 用户实体
    """
    try:
        db.session.commit()
    except OperationalError as e:
        logger.info("update_user errorMsg= {} ".format(e))
        db.session.rollback() 