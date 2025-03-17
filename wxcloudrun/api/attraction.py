from flask import Blueprint, request, jsonify
from wxcloudrun import app, db
from wxcloudrun.model import Attraction

# 创建蓝图
attraction_bp = Blueprint('attraction', __name__)

# 注册蓝图
app.register_blueprint(attraction_bp, url_prefix='/api/attraction')

@attraction_bp.route('/list', methods=['GET'])
def get_attractions():
    """获取景点列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        
        # 构建查询
        query = Attraction.query
        if category:
            query = query.filter_by(category=category)
            
        # 分页
        attractions = query.paginate(page=page, per_page=per_page)
        
        # 格式化返回数据
        result = {
            'code': 0,
            'data': [
                {
                    'id': a.id,
                    'name': a.name,
                    'cover_image': a.cover_image,
                    'description': a.description,
                    'address': a.address,
                    'price': a.price,
                    'category': a.category
                } for a in attractions.items
            ],
            'total': attractions.total,
            'page': page,
            'per_page': per_page
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)})

@attraction_bp.route('/<int:attraction_id>', methods=['GET'])
def get_attraction(attraction_id):
    """获取景点详情"""
    try:
        attraction = Attraction.query.get(attraction_id)
        if not attraction:
            return jsonify({'code': -1, 'msg': '景点不存在'})
        
        # 格式化景点数据
        result = {
            'code': 0,
            'data': {
                'id': attraction.id,
                'name': attraction.name,
                'cover_image': attraction.cover_image,
                'images': attraction.images,  # 可能需要JSON解析
                'description': attraction.description,
                'address': attraction.address,
                'location': attraction.location,
                'price': attraction.price,
                'opening_hours': attraction.opening_hours,
                'tips': attraction.tips,
                'category': attraction.category,
                'created_at': attraction.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)}) 