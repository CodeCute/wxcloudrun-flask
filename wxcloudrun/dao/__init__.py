# 导入所有DAO功能，方便其他模块导入
from wxcloudrun.dao.counter_dao import query_counterbyid, delete_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.dao.user_dao import get_user_by_openid, create_user, update_user
from wxcloudrun.dao.guide_dao import get_travel_guides, get_travel_guide_by_id, create_travel_guide
from wxcloudrun.dao.attraction_dao import get_attractions, get_attraction_by_id, create_attraction
from wxcloudrun.dao.favorite_dao import add_favorite, remove_favorite, get_user_favorites
from wxcloudrun.dao.plan_dao import create_travel_plan, get_user_travel_plans, get_travel_plan_by_id, add_travel_plan_item, get_travel_plan_items 