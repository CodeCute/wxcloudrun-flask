from flask import Blueprint, request, jsonify
from wxcloudrun import app, db
from wxcloudrun.model import Favorite, Attraction, TravelGuide

# 创建蓝图
favorite_bp = Blueprint('favorite', __name__)

# 注册蓝图
app.register_blueprint(favorite_bp, url_prefix='/api/favorite')

@favorite_bp.route('/add', methods=['POST'])
def add_favorite():
    """添加收藏"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        type = data.get('type')  # 'attraction' 或 'guide'
        item_id = data.get('item_id')
        
        if not all([user_id, type, item_id]):
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

@favorite_bp.route('/remove', methods=['POST'])
def remove_favorite():
    """取消收藏"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        type = data.get('type')
        item_id = data.get('item_id')
        
        if not all([user_id, type, item_id]):
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

@favorite_bp.route('/list', methods=['GET'])
def get_favorites():
    """获取用户收藏列表"""
    try:
        user_id = request.args.get('user_id')
        type = request.args.get('type')  # 可选，筛选收藏类型
        
        if not user_id:
            return jsonify({'code': -1, 'msg': '缺少用户ID参数'})
        
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