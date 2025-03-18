from flask import request
from run import app
import logging
from wxcloudrun.model import Feedback, AboutInfo
from wxcloudrun import db
from wxcloudrun.response import make_succ_response, make_err_response
from datetime import datetime

# 配置日志
logger = logging.getLogger('travel-cloud')

# 获取当前用户的openid
def get_openid():
    # 从请求头中获取openid
    openid = request.headers.get('X-WX-OPENID')
    if not openid:
        return None
    return openid

# 提交反馈信息
@app.route('/api/feedback/submit', methods=['POST'])
def submit_feedback():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'type' not in params or 'content' not in params:
            return make_err_response('缺少必要参数')
        
        feedback_type = params.get('type')
        content = params.get('content')
        contact = params.get('contact')
        images = params.get('images', [])
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 处理图片
        images_str = ','.join(images) if images else None
        
        # 创建反馈
        feedback = Feedback(
            user_id=openid,
            type=feedback_type,
            content=content,
            contact=contact,
            images=images_str,
            status=0  # 未处理状态
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        # 返回新创建的反馈
        result = {
            'id': feedback.id,
            'type': feedback.type,
            'content': feedback.content,
            'contact': feedback.contact,
            'images': images,
            'status': feedback.status,
            'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        db.session.rollback()
        logger.error(f"提交反馈失败: {e}")
        return make_err_response(f"提交反馈失败: {str(e)}")

# 获取关于我们信息
@app.route('/api/about/info', methods=['GET'])
def get_about_info():
    try:
        info_type = request.args.get('type', 'company')  # 默认获取公司简介
        
        # 获取指定类型的信息
        info = AboutInfo.query.filter_by(type=info_type).first()
        if not info:
            return make_err_response(f'未找到{info_type}类型的信息')
        
        # 构建返回数据
        result = {
            'id': info.id,
            'title': info.title,
            'content': info.content,
            'type': info.type,
            'updated_at': info.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取关于我们信息失败: {e}")
        return make_err_response(f"获取关于我们信息失败: {str(e)}") 