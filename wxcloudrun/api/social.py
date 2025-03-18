from flask import request
from run import app
import logging
from wxcloudrun.model import UserFollow, User
from wxcloudrun import db
from wxcloudrun.response import make_succ_response, make_err_response

# 配置日志
logger = logging.getLogger('travel-cloud')

# 获取当前用户的openid
def get_openid():
    # 从请求头中获取openid
    openid = request.headers.get('X-WX-OPENID')
    if not openid:
        return None
    return openid

# 关注用户
@app.route('/api/user/follow', methods=['POST'])
def follow_user():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'following_id' not in params:
            return make_err_response('缺少following_id参数')
        
        following_id = params.get('following_id')
        
        # 获取当前用户openid
        follower_id = get_openid()
        if not follower_id:
            return make_err_response('未登录或登录已过期')
        
        # 不能关注自己
        if follower_id == following_id:
            return make_err_response('不能关注自己')
        
        # 检查是否已经关注
        existing_follow = UserFollow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()
        
        if existing_follow:
            return make_err_response('已经关注过该用户')
        
        # 创建关注关系
        new_follow = UserFollow(
            follower_id=follower_id,
            following_id=following_id
        )
        
        db.session.add(new_follow)
        db.session.commit()
        
        return make_succ_response({'success': True})
    except Exception as e:
        db.session.rollback()
        logger.error(f"关注用户失败: {e}")
        return make_err_response(f"关注用户失败: {str(e)}")

# 取消关注
@app.route('/api/user/unfollow', methods=['POST'])
def unfollow_user():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'following_id' not in params:
            return make_err_response('缺少following_id参数')
        
        following_id = params.get('following_id')
        
        # 获取当前用户openid
        follower_id = get_openid()
        if not follower_id:
            return make_err_response('未登录或登录已过期')
        
        # 查找关注关系
        follow = UserFollow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()
        
        if not follow:
            return make_err_response('尚未关注该用户')
        
        # 删除关注关系
        db.session.delete(follow)
        db.session.commit()
        
        return make_succ_response({'success': True})
    except Exception as e:
        db.session.rollback()
        logger.error(f"取消关注失败: {e}")
        return make_err_response(f"取消关注失败: {str(e)}")

# 获取粉丝列表
@app.route('/api/user/followers', methods=['GET'])
def get_followers():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        user_id = request.args.get('user_id')
        
        # 如果没有指定用户id，则获取当前登录用户的粉丝
        if not user_id:
            user_id = get_openid()
            if not user_id:
                return make_err_response('未登录或登录已过期')
        
        # 获取粉丝列表
        followers_query = db.session.query(UserFollow.follower_id).filter_by(following_id=user_id)
        
        # 分页
        total = followers_query.count()
        followers = followers_query.limit(page_size).offset((page - 1) * page_size).all()
        
        # 构建返回结果
        result = {
            'total': total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        # 检查当前登录用户是否关注了这些粉丝
        current_user_id = get_openid()
        
        for follower in followers:
            follower_id = follower[0]
            
            # 获取粉丝基本信息
            user = User.query.filter_by(openid=follower_id).first()
            if not user:
                continue
            
            follower_info = {
                'user_id': follower_id,
                'nickname': user.nickname,
                'avatar': user.avatar,
                'is_following': False
            }
            
            # 检查当前登录用户是否关注了该粉丝
            if current_user_id:
                is_following = UserFollow.query.filter_by(
                    follower_id=current_user_id,
                    following_id=follower_id
                ).first() is not None
                
                follower_info['is_following'] = is_following
            
            result['list'].append(follower_info)
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取粉丝列表失败: {e}")
        return make_err_response(f"获取粉丝列表失败: {str(e)}")

# 获取关注列表
@app.route('/api/user/following', methods=['GET'])
def get_following():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        user_id = request.args.get('user_id')
        
        # 如果没有指定用户id，则获取当前登录用户的关注
        if not user_id:
            user_id = get_openid()
            if not user_id:
                return make_err_response('未登录或登录已过期')
        
        # 获取关注列表
        following_query = db.session.query(UserFollow.following_id).filter_by(follower_id=user_id)
        
        # 分页
        total = following_query.count()
        following = following_query.limit(page_size).offset((page - 1) * page_size).all()
        
        # 构建返回结果
        result = {
            'total': total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        for follow in following:
            following_id = follow[0]
            
            # 获取被关注者基本信息
            user = User.query.filter_by(openid=following_id).first()
            if not user:
                continue
            
            following_info = {
                'user_id': following_id,
                'nickname': user.nickname,
                'avatar': user.avatar
            }
            
            result['list'].append(following_info)
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取关注列表失败: {e}")
        return make_err_response(f"获取关注列表失败: {str(e)}") 