from flask import request, g
from run import app
import logging
from wxcloudrun.model import News, NewsLike, NewsComment
from wxcloudrun import db
from wxcloudrun.response import make_succ_response, make_err_response
from datetime import datetime

# 配置日志
logger = logging.getLogger('travel-cloud')

# 获取当前用户的openid的装饰器
def get_openid():
    # 从请求头中获取openid
    openid = request.headers.get('X-WX-OPENID')
    if not openid:
        return None
    return openid

# 获取资讯/动态列表
@app.route('/api/news/list', methods=['GET'])
def get_news_list():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        category = request.args.get('category')
        
        # 构建查询
        query = News.query
        
        # 如果提供了分类，按分类筛选
        if category:
            query = query.filter_by(category=category)
        
        # 按创建时间倒序排序并分页
        news_list = query.order_by(News.createdAt.desc()).paginate(
            page=page, per_page=page_size
        )
        
        # 构建返回结果
        result = {
            'total': news_list.total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        # 处理用户点赞状态
        openid = get_openid()
        
        for news in news_list.items:
            item = {
                'id': news.id,
                'title': news.title,
                'cover_image': news.cover_image,
                'author_id': news.author_id,
                'view_count': news.view_count,
                'like_count': news.like_count,
                'comment_count': news.comment_count,
                'created_at': news.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
                'is_liked': False
            }
            
            # 如果有用户登录，检查是否点赞过
            if openid:
                like = NewsLike.query.filter_by(news_id=news.id, user_id=openid).first()
                if like:
                    item['is_liked'] = True
            
            result['list'].append(item)
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取资讯列表失败: {e}")
        return make_err_response(f"获取资讯列表失败: {str(e)}")

# 获取资讯/动态详情
@app.route('/api/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    try:
        news = News.query.get(news_id)
        if not news:
            return make_err_response('资讯不存在')
        
        # 增加浏览次数
        news.view_count += 1
        db.session.commit()
        
        # 构建返回数据
        result = {
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'cover_image': news.cover_image,
            'author_id': news.author_id,
            'view_count': news.view_count,
            'like_count': news.like_count,
            'comment_count': news.comment_count,
            'created_at': news.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': news.updatedAt.strftime('%Y-%m-%d %H:%M:%S'),
            'is_liked': False
        }
        
        # 获取当前用户是否点赞
        openid = get_openid()
        if openid:
            like = NewsLike.query.filter_by(news_id=news_id, user_id=openid).first()
            if like:
                result['is_liked'] = True
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取资讯详情失败: {e}")
        return make_err_response(f"获取资讯详情失败: {str(e)}")

# 点赞资讯/动态
@app.route('/api/news/like', methods=['POST'])
def like_news():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'news_id' not in params:
            return make_err_response('缺少参数news_id')
        
        news_id = params['news_id']
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 检查资讯是否存在
        news = News.query.get(news_id)
        if not news:
            return make_err_response('资讯不存在')
        
        # 检查是否已经点赞
        like = NewsLike.query.filter_by(news_id=news_id, user_id=openid).first()
        if like:
            return make_err_response('已经点赞过')
        
        # 创建点赞记录
        new_like = NewsLike(news_id=news_id, user_id=openid)
        db.session.add(new_like)
        
        # 更新资讯点赞数
        news.like_count += 1
        
        db.session.commit()
        
        return make_succ_response({'like_count': news.like_count})
    except Exception as e:
        db.session.rollback()
        logger.error(f"点赞资讯失败: {e}")
        return make_err_response(f"点赞资讯失败: {str(e)}")

# 取消点赞
@app.route('/api/news/unlike', methods=['POST'])
def unlike_news():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'news_id' not in params:
            return make_err_response('缺少参数news_id')
        
        news_id = params['news_id']
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 检查资讯是否存在
        news = News.query.get(news_id)
        if not news:
            return make_err_response('资讯不存在')
        
        # 检查是否已经点赞
        like = NewsLike.query.filter_by(news_id=news_id, user_id=openid).first()
        if not like:
            return make_err_response('尚未点赞')
        
        # 删除点赞记录
        db.session.delete(like)
        
        # 更新资讯点赞数
        if news.like_count > 0:
            news.like_count -= 1
        
        db.session.commit()
        
        return make_succ_response({'like_count': news.like_count})
    except Exception as e:
        db.session.rollback()
        logger.error(f"取消点赞失败: {e}")
        return make_err_response(f"取消点赞失败: {str(e)}")

# 获取评论列表
@app.route('/api/news/comments/<int:news_id>', methods=['GET'])
def get_news_comments(news_id):
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        # 获取一级评论
        comments = NewsComment.query.filter_by(
            news_id=news_id, 
            parent_id=None
        ).order_by(
            NewsComment.createdAt.desc()
        ).paginate(
            page=page, per_page=page_size
        )
        
        # 构建返回结果
        result = {
            'total': comments.total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        for comment in comments.items:
            # 查询该评论的回复
            replies = NewsComment.query.filter_by(
                parent_id=comment.id
            ).order_by(
                NewsComment.createdAt.asc()
            ).all()
            
            # 格式化回复
            formatted_replies = []
            for reply in replies:
                formatted_replies.append({
                    'id': reply.id,
                    'user_id': reply.user_id,
                    'content': reply.content,
                    'created_at': reply.createdAt.strftime('%Y-%m-%d %H:%M:%S')
                })
            
            # 添加到结果列表
            result['list'].append({
                'id': comment.id,
                'user_id': comment.user_id,
                'content': comment.content,
                'created_at': comment.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
                'replies': formatted_replies
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取评论列表失败: {e}")
        return make_err_response(f"获取评论列表失败: {str(e)}")

# 发布评论
@app.route('/api/news/comment', methods=['POST'])
def post_news_comment():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'news_id' not in params or 'content' not in params:
            return make_err_response('缺少必要参数')
        
        news_id = params.get('news_id')
        content = params.get('content')
        parent_id = params.get('parent_id')  # 可选，回复的评论ID
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 检查资讯是否存在
        news = News.query.get(news_id)
        if not news:
            return make_err_response('资讯不存在')
        
        # 检查父评论是否存在
        if parent_id:
            parent_comment = NewsComment.query.get(parent_id)
            if not parent_comment:
                return make_err_response('回复的评论不存在')
        
        # 创建评论
        new_comment = NewsComment(
            news_id=news_id,
            user_id=openid,
            content=content,
            parent_id=parent_id
        )
        
        db.session.add(new_comment)
        
        # 更新资讯评论数
        news.comment_count += 1
        
        db.session.commit()
        
        # 返回新创建的评论
        result = {
            'id': new_comment.id,
            'user_id': new_comment.user_id,
            'content': new_comment.content,
            'parent_id': new_comment.parent_id,
            'created_at': new_comment.createdAt.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        db.session.rollback()
        logger.error(f"发布评论失败: {e}")
        return make_err_response(f"发布评论失败: {str(e)}") 