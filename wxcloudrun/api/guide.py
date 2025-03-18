from flask import request
from run import app
from wxcloudrun.dao import get_travel_guides, get_travel_guide_by_id, create_travel_guide
from wxcloudrun.dao import get_user_favorites, get_user_by_openid
from wxcloudrun.models import TravelGuide
from wxcloudrun.common.response import make_succ_response, make_err_response


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
    
    # 从请求头获取openid
    openid = request.headers.get('x-wx-openid', '')
    if openid:
        # 获取用户ID
        user = get_user_by_openid(openid)
        if user:
            user_id = user.id
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