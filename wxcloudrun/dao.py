import logging
import json
from sqlalchemy.exc import OperationalError

from wxcloudrun import db
from wxcloudrun.model import Counters, User, TravelGuide, Attraction, Favorite, TravelPlan, TravelPlanItem

# 初始化日志
logger = logging.getLogger('log')


def query_counterbyid(id):
    """
    根据ID查询Counter实体
    :param id: Counter的ID
    :return: Counter实体
    """
    try:
        return Counters.query.filter(Counters.id == id).first()
    except OperationalError as e:
        logger.info("query_counterbyid errorMsg= {} ".format(e))
        return None


def delete_counterbyid(id):
    """
    根据ID删除Counter实体
    :param id: Counter的ID
    """
    try:
        counter = Counters.query.get(id)
        if counter is None:
            return
        db.session.delete(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("delete_counterbyid errorMsg= {} ".format(e))


def insert_counter(counter):
    """
    插入一个Counter实体
    :param counter: Counters实体
    """
    try:
        db.session.add(counter)
        db.session.commit()
    except OperationalError as e:
        logger.info("insert_counter errorMsg= {} ".format(e))


def update_counterbyid(counter):
    """
    根据ID更新counter的值
    :param counter实体
    """
    try:
        counter = query_counterbyid(counter.id)
        if counter is None:
            return
        db.session.flush()
        db.session.commit()
    except OperationalError as e:
        logger.info("update_counterbyid errorMsg= {} ".format(e))


# 用户相关数据访问方法
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


# 旅游指南相关数据访问方法
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


# 景点相关数据访问方法
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


# 收藏相关数据访问方法
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


# 行程计划相关数据访问方法
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
