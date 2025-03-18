from flask import request
from run import app
from wxcloudrun.dao import get_user_by_openid, create_user, update_user
from wxcloudrun.models import User
from wxcloudrun.common.response import make_succ_response, make_err_response


@app.route('/api/user/login', methods=['POST'])
def user_login():
    """
    用户登录接口
    前端通过 wx.login() 获取 code，后端通过 code 换取 openid
    或直接从请求头获取微信云托管环境提供的openid
    """
    params = request.get_json()
    
    # 尝试从请求头获取openid（微信云托管环境会自动注入）
    openid = request.headers.get('x-wx-openid', '')
    
    # 如果请求头中没有openid，则使用传统方式（code换取openid）
    if not openid and 'code' in params:
        code = params['code']
        # 实际项目中，这里应该调用微信的api获取openid
        # 此处仅作为示例，使用code作为openid
        openid = code
    
    if not openid:
        return make_err_response('无法获取用户标识')
    
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
    从请求头获取openid
    """
    params = request.get_json()
    
    # 从请求头获取openid
    openid = request.headers.get('x-wx-openid', '')
    if not openid:
        return make_err_response('缺少openid参数')
    
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
    从请求头中获取openid
    """
    # 从请求头中获取openid
    openid = request.headers.get('x-wx-openid', '')
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