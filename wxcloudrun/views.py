from datetime import datetime
import json
import os
import random
from flask import render_template, request, g
from run import app
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


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


# -------------------- 用户相关接口 --------------------

@app.route('/api/user/login', methods=['POST'])
def user_login():
    """
    用户登录接口
    前端通过 wx.login() 获取 code，后端通过 code 换取 openid
    """
    params = request.get_json()
    
    # 小程序登录
    if 'code' not in params:
        return make_err_response('缺少code参数')
    
    code = params['code']
    # 实际项目中，这里应该调用微信的api获取openid
    # 此处仅作为示例，使用code作为openid
    openid = code
    
    # 查询用户是否存在，不存在则创建用户
    user = get_user_by_openid(openid)
    if user is None:
        user = User()
        user.openid = openid
        if 'userInfo' in params:
            user_info = params['userInfo']
            user.nickname = user_info.get('nickName', '')
            user.avatar = user_info.get('avatarUrl', '')
            user.gender = user_info.get('gender', 0)
        user_id = create_user(user)
        if not user_id:
            return make_err_response('创建用户失败')
    else:
        # 更新用户信息
        if 'userInfo' in params:
            user_info = params['userInfo']
            user.nickname = user_info.get('nickName', user.nickname)
            user.avatar = user_info.get('avatarUrl', user.avatar)
            user.gender = user_info.get('gender', user.gender)
            update_user(user)
    
    # 返回用户信息和登录态
    return make_succ_response({
        'openid': openid,
        'userId': user.id,
        'userInfo': {
            'nickname': user.nickname,
            'avatar': user.avatar,
            'gender': user.gender,
            'phone': user.phone
        }
    })

@app.route('/api/user/update', methods=['POST'])
def update_user_info():
    """
    更新用户信息
    """
    params = request.get_json()
    
    if 'openid' not in params:
        return make_err_response('缺少openid参数')
    
    openid = params['openid']
    user = get_user_by_openid(openid)
    if user is None:
        return make_err_response('用户不存在')
    
    # 更新用户信息
    if 'nickname' in params:
        user.nickname = params['nickname']
    if 'avatar' in params:
        user.avatar = params['avatar']
    if 'gender' in params:
        user.gender = params['gender']
    if 'phone' in params:
        user.phone = params['phone']
    
    update_user(user)
    
    return make_succ_response({
        'userId': user.id,
        'userInfo': {
            'nickname': user.nickname,
            'avatar': user.avatar,
            'gender': user.gender,
            'phone': user.phone
        }
    })

@app.route('/api/user/info', methods=['GET'])
def get_user_info():
    """
    获取用户信息
    """
    openid = request.args.get('openid', '')
    if not openid:
        return make_err_response('缺少openid参数')
    
    user = get_user_by_openid(openid)
    if user is None:
        return make_err_response('用户不存在')
    
    return make_succ_response({
        'userId': user.id,
        'userInfo': {
            'nickname': user.nickname,
            'avatar': user.avatar,
            'gender': user.gender,
            'phone': user.phone
        }
    })


# -------------------- 旅游指南相关接口 --------------------

@app.route('/api/guides', methods=['GET'])
def get_guides():
    """
    获取旅游指南列表
    """
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    
    guides = get_travel_guides(page, page_size)
    
    result = []
    for guide in guides:
        result.append({
            'id': guide.id,
            'title': guide.title,
            'coverImage': guide.cover_image,
            'description': guide.description,
            'author': guide.author,
            'viewCount': guide.view_count,
            'likeCount': guide.like_count,
            'createdAt': guide.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return make_succ_response(result)

@app.route('/api/guides/<int:guide_id>', methods=['GET'])
def get_guide_detail(guide_id):
    """
    获取旅游指南详情
    """
    guide = get_travel_guide_by_id(guide_id)
    
    if guide is None:
        return make_err_response('旅游指南不存在')
    
    # 检查用户是否已收藏
    is_favorite = False
    user_id = request.args.get('userId', '')
    if user_id:
        favorites = get_user_favorites(user_id, 'guide')
        for fav in favorites:
            if fav.item_id == guide_id:
                is_favorite = True
                break
    
    result = {
        'id': guide.id,
        'title': guide.title,
        'coverImage': guide.cover_image,
        'description': guide.description,
        'content': guide.content,
        'author': guide.author,
        'viewCount': guide.view_count,
        'likeCount': guide.like_count,
        'isFavorite': is_favorite,
        'createdAt': guide.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return make_succ_response(result)

@app.route('/api/guides', methods=['POST'])
def create_guide():
    """
    创建旅游指南（管理员接口）
    """
    params = request.get_json()
    
    # 必填字段校验
    if 'title' not in params:
        return make_err_response('缺少title参数')
    
    guide = TravelGuide()
    guide.title = params['title']
    guide.cover_image = params.get('coverImage', '')
    guide.description = params.get('description', '')
    guide.content = params.get('content', '')
    guide.author = params.get('author', '')
    
    guide_id = create_travel_guide(guide)
    if not guide_id:
        return make_err_response('创建旅游指南失败')
    
    return make_succ_response({'guideId': guide_id})


# -------------------- 景点相关接口 --------------------

@app.route('/api/attractions', methods=['GET'])
def get_attraction_list():
    """
    获取景点列表
    """
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('pageSize', 10))
    category = request.args.get('category', '')
    
    attractions = get_attractions(page, page_size, category if category else None)
    
    result = []
    for attraction in attractions:
        result.append({
            'id': attraction.id,
            'name': attraction.name,
            'coverImage': attraction.cover_image,
            'description': attraction.description,
            'address': attraction.address,
            'price': attraction.price,
            'category': attraction.category,
            'createdAt': attraction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return make_succ_response(result)

@app.route('/api/attractions/<int:attraction_id>', methods=['GET'])
def get_attraction_detail(attraction_id):
    """
    获取景点详情
    """
    attraction = get_attraction_by_id(attraction_id)
    
    if attraction is None:
        return make_err_response('景点不存在')
    
    # 检查用户是否已收藏
    is_favorite = False
    user_id = request.args.get('userId', '')
    if user_id:
        favorites = get_user_favorites(user_id, 'attraction')
        for fav in favorites:
            if fav.item_id == attraction_id:
                is_favorite = True
                break
    
    # 解析图片列表
    images = []
    if attraction.images:
        try:
            images = json.loads(attraction.images)
        except:
            pass
    
    result = {
        'id': attraction.id,
        'name': attraction.name,
        'coverImage': attraction.cover_image,
        'images': images,
        'description': attraction.description,
        'address': attraction.address,
        'location': attraction.location,
        'price': attraction.price,
        'openingHours': attraction.opening_hours,
        'tips': attraction.tips,
        'category': attraction.category,
        'isFavorite': is_favorite,
        'createdAt': attraction.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return make_succ_response(result)

@app.route('/api/attractions', methods=['POST'])
def create_attraction_api():
    """
    创建景点（管理员接口）
    """
    params = request.get_json()
    
    # 必填字段校验
    if 'name' not in params:
        return make_err_response('缺少name参数')
    
    attraction = Attraction()
    attraction.name = params['name']
    attraction.cover_image = params.get('coverImage', '')
    
    # 处理图片列表
    if 'images' in params and isinstance(params['images'], list):
        attraction.images = json.dumps(params['images'])
    
    attraction.description = params.get('description', '')
    attraction.address = params.get('address', '')
    attraction.location = params.get('location', '')
    attraction.price = params.get('price', 0)
    attraction.opening_hours = params.get('openingHours', '')
    attraction.tips = params.get('tips', '')
    attraction.category = params.get('category', '')
    
    attraction_id = create_attraction(attraction)
    if not attraction_id:
        return make_err_response('创建景点失败')
    
    return make_succ_response({'attractionId': attraction_id})


# -------------------- 收藏相关接口 --------------------

@app.route('/api/favorites/add', methods=['POST'])
def add_to_favorite():
    """
    添加收藏
    """
    params = request.get_json()
    
    # 必填字段校验
    if 'userId' not in params:
        return make_err_response('缺少userId参数')
    if 'type' not in params:
        return make_err_response('缺少type参数')
    if 'itemId' not in params:
        return make_err_response('缺少itemId参数')
    
    user_id = params['userId']
    item_type = params['type']
    item_id = params['itemId']
    
    # 类型限制
    if item_type not in ['guide', 'attraction']:
        return make_err_response('type参数错误，只支持guide和attraction')
    
    # 查询是否已收藏
    favorites = get_user_favorites(user_id, item_type)
    for fav in favorites:
        if fav.item_id == item_id:
            return make_succ_response({'favoriteId': fav.id})
    
    # 添加收藏
    favorite = Favorite()
    favorite.user_id = user_id
    favorite.type = item_type
    favorite.item_id = item_id
    
    favorite_id = add_favorite(favorite)
    if not favorite_id:
        return make_err_response('添加收藏失败')
    
    return make_succ_response({'favoriteId': favorite_id})

@app.route('/api/favorites/remove', methods=['POST'])
def remove_from_favorite():
    """
    取消收藏
    """
    params = request.get_json()
    
    # 必填字段校验
    if 'userId' not in params:
        return make_err_response('缺少userId参数')
    if 'type' not in params:
        return make_err_response('缺少type参数')
    if 'itemId' not in params:
        return make_err_response('缺少itemId参数')
    
    user_id = params['userId']
    item_type = params['type']
    item_id = params['itemId']
    
    # 取消收藏
    remove_favorite(user_id, item_type, item_id)
    
    return make_succ_empty_response()

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """
    获取收藏列表
    """
    user_id = request.args.get('userId', '')
    if not user_id:
        return make_err_response('缺少userId参数')
    
    item_type = request.args.get('type', '')
    
    favorites = get_user_favorites(user_id, item_type if item_type else None)
    
    result = []
    for fav in favorites:
        item = None
        if fav.type == 'guide':
            item = get_travel_guide_by_id(fav.item_id)
            if item:
                result.append({
                    'id': fav.id,
                    'type': fav.type,
                    'itemId': fav.item_id,
                    'item': {
                        'id': item.id,
                        'title': item.title,
                        'coverImage': item.cover_image,
                        'description': item.description
                    },
                    'createdAt': fav.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
        elif fav.type == 'attraction':
            item = get_attraction_by_id(fav.item_id)
            if item:
                result.append({
                    'id': fav.id,
                    'type': fav.type,
                    'itemId': fav.item_id,
                    'item': {
                        'id': item.id,
                        'name': item.name,
                        'coverImage': item.cover_image,
                        'description': item.description
                    },
                    'createdAt': fav.created_at.strftime('%Y-%m-%d %H:%M:%S')
                })
    
    return make_succ_response(result)


# -------------------- 行程计划相关接口 --------------------

@app.route('/api/plans', methods=['POST'])
def create_plan():
    """
    创建行程计划
    """
    params = request.get_json()
    
    # 必填字段校验
    if 'userId' not in params:
        return make_err_response('缺少userId参数')
    if 'title' not in params:
        return make_err_response('缺少title参数')
    
    plan = TravelPlan()
    plan.user_id = params['userId']
    plan.title = params['title']
    
    if 'startDate' in params:
        try:
            plan.start_date = datetime.strptime(params['startDate'], '%Y-%m-%d').date()
        except:
            return make_err_response('startDate格式错误，应为YYYY-MM-DD')
    
    if 'endDate' in params:
        try:
            plan.end_date = datetime.strptime(params['endDate'], '%Y-%m-%d').date()
        except:
            return make_err_response('endDate格式错误，应为YYYY-MM-DD')
    
    plan.description = params.get('description', '')
    
    plan_id = create_travel_plan(plan)
    if not plan_id:
        return make_err_response('创建行程计划失败')
    
    # 创建行程项目
    if 'items' in params and isinstance(params['items'], list):
        for item in params['items']:
            plan_item = TravelPlanItem()
            plan_item.plan_id = plan_id
            plan_item.day = item.get('day', 1)
            plan_item.attraction_id = item.get('attractionId')
            plan_item.time_period = item.get('timePeriod', '')
            plan_item.note = item.get('note', '')
            add_travel_plan_item(plan_item)
    
    return make_succ_response({'planId': plan_id})

@app.route('/api/plans', methods=['GET'])
def get_plans():
    """
    获取用户行程计划列表
    """
    user_id = request.args.get('userId', '')
    if not user_id:
        return make_err_response('缺少userId参数')
    
    plans = get_user_travel_plans(user_id)
    
    result = []
    for plan in plans:
        result.append({
            'id': plan.id,
            'title': plan.title,
            'startDate': plan.start_date.strftime('%Y-%m-%d') if plan.start_date else '',
            'endDate': plan.end_date.strftime('%Y-%m-%d') if plan.end_date else '',
            'description': plan.description,
            'createdAt': plan.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return make_succ_response(result)

@app.route('/api/plans/<int:plan_id>', methods=['GET'])
def get_plan_detail(plan_id):
    """
    获取行程计划详情
    """
    plan = get_travel_plan_by_id(plan_id)
    
    if plan is None:
        return make_err_response('行程计划不存在')
    
    # 获取行程项目
    plan_items = get_travel_plan_items(plan_id)
    
    items = []
    for item in plan_items:
        attraction = None
        if item.attraction_id:
            attraction = get_attraction_by_id(item.attraction_id)
        
        items.append({
            'id': item.id,
            'day': item.day,
            'attractionId': item.attraction_id,
            'attraction': {
                'id': attraction.id,
                'name': attraction.name,
                'coverImage': attraction.cover_image,
                'address': attraction.address
            } if attraction else None,
            'timePeriod': item.time_period,
            'note': item.note
        })
    
    result = {
        'id': plan.id,
        'title': plan.title,
        'startDate': plan.start_date.strftime('%Y-%m-%d') if plan.start_date else '',
        'endDate': plan.end_date.strftime('%Y-%m-%d') if plan.end_date else '',
        'description': plan.description,
        'items': items,
        'createdAt': plan.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return make_succ_response(result)

@app.route('/api/plans/<int:plan_id>/items', methods=['POST'])
def add_plan_item():
    """
    添加行程项目
    """
    plan_id = plan_id
    params = request.get_json()
    
    # 检查行程是否存在
    plan = get_travel_plan_by_id(plan_id)
    if plan is None:
        return make_err_response('行程计划不存在')
    
    # 必填字段校验
    if 'day' not in params:
        return make_err_response('缺少day参数')
    
    plan_item = TravelPlanItem()
    plan_item.plan_id = plan_id
    plan_item.day = params['day']
    plan_item.attraction_id = params.get('attractionId')
    plan_item.time_period = params.get('timePeriod', '')
    plan_item.note = params.get('note', '')
    
    item_id = add_travel_plan_item(plan_item)
    if not item_id:
        return make_err_response('添加行程项目失败')
    
    return make_succ_response({'itemId': item_id})


# -------------------- 数据初始化相关接口 --------------------

@app.route('/api/initialize', methods=['POST'])
def initialize_data():
    """
    初始化示例数据（仅用于演示）
    """
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
        create_travel_guide(guide)
    
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
        create_attraction(attraction)
    
    return make_succ_response({"message": "数据初始化成功！"})
