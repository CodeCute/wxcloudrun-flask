from flask import request, jsonify
from wxcloudrun import app, db
from wxcloudrun.model import Favorite, Attraction, TravelGuide
from wxcloudrun.dao import get_user_by_openid, get_attraction_by_id, get_travel_guide_by_id, get_user_favorites
from wxcloudrun.common.response import make_succ_response, make_err_response

@app.route('/api/favorite/add', methods=['POST'])
def add_favorite():
    """添加收藏 (从请求头获取openid)"""
    try:
        # 从请求头获取openid
        openid = request.headers.get('x-wx-openid', '')
        if not openid:
            return jsonify({'code': -1, 'msg': '缺少用户标识'})
        
        # 根据openid查询用户
        user = get_user_by_openid(openid)
        if not user:
            return jsonify({'code': -1, 'msg': '用户不存在'})
        
        user_id = user.id
        data = request.get_json()
        type = data.get('type')  # 'attraction' 或 'guide'
        item_id = data.get('item_id')
        
        if not all([type, item_id]):
            return jsonify({'code': -1, 'msg': '缺少必要参数'})
        
        # 检查收藏对象是否存在
        if type == 'attraction':
            item = Attraction.query.get(item_id)
            if not item:
                return jsonify({'code': -1, 'msg': '景点不存在'})
        elif type == 'guide':
            item = TravelGuide.query.get(item_id)
            if not item:
                return jsonify({'code': -1, 'msg': '旅游指南不存在'})
        else:
            return jsonify({'code': -1, 'msg': '收藏类型错误'})
        
        # 检查是否已经收藏
        existing = Favorite.query.filter_by(user_id=user_id, type=type, item_id=item_id).first()
        if existing:
            return jsonify({'code': -1, 'msg': '已经收藏过该内容'})
        
        # 添加收藏
        favorite = Favorite(user_id=user_id, type=type, item_id=item_id)
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({'code': 0, 'msg': '收藏成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/favorite/remove', methods=['POST'])
def remove_favorite():
    """取消收藏 (从请求头获取openid)"""
    try:
        # 从请求头获取openid
        openid = request.headers.get('x-wx-openid', '')
        if not openid:
            return jsonify({'code': -1, 'msg': '缺少用户标识'})
        
        # 根据openid查询用户
        user = get_user_by_openid(openid)
        if not user:
            return jsonify({'code': -1, 'msg': '用户不存在'})
        
        user_id = user.id
        data = request.get_json()
        type = data.get('type')
        item_id = data.get('item_id')
        
        if not all([type, item_id]):
            return jsonify({'code': -1, 'msg': '缺少必要参数'})
        
        # 查找收藏记录
        favorite = Favorite.query.filter_by(user_id=user_id, type=type, item_id=item_id).first()
        if not favorite:
            return jsonify({'code': -1, 'msg': '未找到收藏记录'})
        
        # 删除收藏
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({'code': 0, 'msg': '取消收藏成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/favorite/list', methods=['GET'])
def get_favorites():
    """获取用户收藏列表 (从请求头获取openid)"""
    try:
        # 从请求头获取openid
        openid = request.headers.get('x-wx-openid', '')
        if not openid:
            return jsonify({'code': -1, 'msg': '缺少用户标识'})
        
        # 根据openid查询用户
        user = get_user_by_openid(openid)
        if not user:
            return jsonify({'code': -1, 'msg': '用户不存在'})
        
        user_id = user.id
        type = request.args.get('type')  # 可选，筛选收藏类型
        
        # 构建查询
        query = Favorite.query.filter_by(user_id=user_id)
        if type:
            query = query.filter_by(type=type)
        
        favorites = query.all()
        result = {'code': 0, 'data': []}
        
        # 获取收藏内容的详情
        for fav in favorites:
            if fav.type == 'attraction':
                item = Attraction.query.get(fav.item_id)
                if item:
                    result['data'].append({
                        'id': fav.id,
                        'type': fav.type,
                        'item_id': fav.item_id,
                        'created_at': fav.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'item': {
                            'id': item.id,
                            'name': item.name,
                            'cover_image': item.cover_image,
                            'description': item.description
                        }
                    })
            elif fav.type == 'guide':
                item = TravelGuide.query.get(fav.item_id)
                if item:
                    result['data'].append({
                        'id': fav.id,
                        'type': fav.type,
                        'item_id': fav.item_id,
                        'created_at': fav.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'item': {
                            'id': item.id,
                            'title': item.title,
                            'cover_image': item.cover_image,
                            'description': item.description
                        }
                    })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/favorites', methods=['GET'])
def get_user_favorites_api():
    """
    获取用户收藏列表
    从请求头获取用户ID
    """
    # 从请求头获取openid
    openid = request.headers.get('x-wx-openid', '')
    if not openid:
        return make_err_response('缺少用户标识')
    
    # 根据openid查询用户ID
    user = get_user_by_openid(openid)
    if not user:
        return make_err_response('用户不存在')
    
    user_id = user.id
    type = request.args.get('type')  # 可选，筛选收藏类型
    
    # 获取用户收藏
    favorites = get_user_favorites(user_id, type)
    
    # 构建响应数据
    favorite_list = []
    for fav in favorites:
        item_info = None
        
        # 获取收藏项目详情
        if fav.type == 'attraction':
            attraction = get_attraction_by_id(fav.item_id)
            if attraction:
                item_info = {
                    'id': attraction.id,
                    'name': attraction.name,
                    'coverImage': attraction.cover_image,
                    'description': attraction.description,
                    'address': attraction.address,
                    'category': attraction.category
                }
        elif fav.type == 'guide':
            guide = get_travel_guide_by_id(fav.item_id)
            if guide:
                item_info = {
                    'id': guide.id,
                    'title': guide.title,
                    'coverImage': guide.cover_image,
                    'description': guide.description,
                    'author': guide.author
                }
        
        if item_info:
            favorite_list.append({
                'id': fav.id,
                'type': fav.type,
                'itemId': fav.item_id,
                'item': item_info,
                'createdAt': fav.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    
    return make_succ_response(favorite_list) 