from flask import request
from run import app
import logging
from wxcloudrun.model import Companion, CompanionTag, CompanionTagRelation, CompanionReservation, CompanionReview
from wxcloudrun import db
from wxcloudrun.response import make_succ_response, make_err_response
from datetime import datetime
from sqlalchemy import func

# 配置日志
logger = logging.getLogger('travel-cloud')

# 获取当前用户的openid
def get_openid():
    # 从请求头中获取openid
    openid = request.headers.get('X-WX-OPENID')
    if not openid:
        return None
    return openid

# 获取结伴旅行向导列表
@app.route('/api/companion/list', methods=['GET'])
def get_companion_list():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        location = request.args.get('location')
        tag_id = request.args.get('tag_id')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        
        # 构建查询
        query = Companion.query.filter(Companion.status == 1)  # 只查询活跃的向导
        
        # 按地点筛选
        if location:
            query = query.filter(Companion.location.like(f'%{location}%'))
        
        # 按标签筛选
        if tag_id:
            query = query.join(
                CompanionTagRelation, 
                CompanionTagRelation.companion_id == Companion.id
            ).filter(
                CompanionTagRelation.tag_id == tag_id
            )
        
        # 按价格范围筛选
        if min_price:
            query = query.filter(Companion.price >= float(min_price))
        if max_price:
            query = query.filter(Companion.price <= float(max_price))
        
        # 按评分降序排序
        companions = query.order_by(Companion.rating.desc()).paginate(
            page=page, per_page=page_size
        )
        
        # 构建返回结果
        result = {
            'total': companions.total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        for companion in companions.items:
            # 获取向导标签
            tags = db.session.query(CompanionTag).join(
                CompanionTagRelation,
                CompanionTagRelation.tag_id == CompanionTag.id
            ).filter(
                CompanionTagRelation.companion_id == companion.id
            ).all()
            
            # 格式化标签
            formatted_tags = [{'id': tag.id, 'name': tag.name} for tag in tags]
            
            # 添加到结果列表
            result['list'].append({
                'id': companion.id,
                'user_id': companion.user_id,
                'title': companion.title,
                'avatar': companion.avatar,
                'cover_image': companion.cover_image,
                'price': float(companion.price),
                'location': companion.location,
                'languages': companion.languages,
                'rating': float(companion.rating),
                'review_count': companion.review_count,
                'tags': formatted_tags
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取向导列表失败: {e}")
        return make_err_response(f"获取向导列表失败: {str(e)}")

# 获取向导详情
@app.route('/api/companion/<int:companion_id>', methods=['GET'])
def get_companion_detail(companion_id):
    try:
        companion = Companion.query.get(companion_id)
        if not companion:
            return make_err_response('向导不存在')
        
        # 获取向导标签
        tags = db.session.query(CompanionTag).join(
            CompanionTagRelation,
            CompanionTagRelation.tag_id == CompanionTag.id
        ).filter(
            CompanionTagRelation.companion_id == companion_id
        ).all()
        
        # 获取向导评价
        reviews = CompanionReview.query.filter_by(
            companion_id=companion_id
        ).order_by(
            CompanionReview.created_at.desc()
        ).limit(5).all()
        
        # 格式化标签和评价
        formatted_tags = [{'id': tag.id, 'name': tag.name} for tag in tags]
        formatted_reviews = []
        
        for review in reviews:
            formatted_reviews.append({
                'id': review.id,
                'user_id': review.user_id,
                'rating': float(review.rating),
                'content': review.content,
                'images': review.images.split(',') if review.images else [],
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # 构建返回数据
        result = {
            'id': companion.id,
            'user_id': companion.user_id,
            'title': companion.title,
            'description': companion.description,
            'avatar': companion.avatar,
            'cover_image': companion.cover_image,
            'price': float(companion.price),
            'location': companion.location,
            'experience_years': companion.experience_years,
            'languages': companion.languages,
            'rating': float(companion.rating),
            'review_count': companion.review_count,
            'status': companion.status,
            'created_at': companion.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'tags': formatted_tags,
            'reviews': formatted_reviews
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取向导详情失败: {e}")
        return make_err_response(f"获取向导详情失败: {str(e)}")

# 获取向导标签列表
@app.route('/api/companion/tags', methods=['GET'])
def get_companion_tags():
    try:
        tags = CompanionTag.query.all()
        
        # 构建返回结果
        result = []
        for tag in tags:
            result.append({
                'id': tag.id,
                'name': tag.name
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取向导标签失败: {e}")
        return make_err_response(f"获取向导标签失败: {str(e)}")

# 预约向导服务
@app.route('/api/companion/reserve', methods=['POST'])
def reserve_companion():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'companion_id' not in params or 'start_date' not in params or 'end_date' not in params:
            return make_err_response('缺少必要参数')
        
        companion_id = params.get('companion_id')
        start_date = datetime.strptime(params.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(params.get('end_date'), '%Y-%m-%d').date()
        traveler_count = params.get('traveler_count', 1)
        special_needs = params.get('special_needs')
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 检查向导是否存在
        companion = Companion.query.get(companion_id)
        if not companion:
            return make_err_response('向导不存在')
        
        # 检查日期是否有效
        if start_date > end_date:
            return make_err_response('结束日期不能早于开始日期')
        
        if start_date < datetime.now().date():
            return make_err_response('开始日期不能早于当前日期')
        
        # 创建预约
        reservation = CompanionReservation(
            companion_id=companion_id,
            user_id=openid,
            start_date=start_date,
            end_date=end_date,
            traveler_count=traveler_count,
            special_needs=special_needs,
            status=0  # 待确认状态
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        # 返回新创建的预约
        result = {
            'id': reservation.id,
            'companion_id': reservation.companion_id,
            'start_date': reservation.start_date.strftime('%Y-%m-%d'),
            'end_date': reservation.end_date.strftime('%Y-%m-%d'),
            'traveler_count': reservation.traveler_count,
            'special_needs': reservation.special_needs,
            'status': reservation.status,
            'created_at': reservation.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        db.session.rollback()
        logger.error(f"预约向导失败: {e}")
        return make_err_response(f"预约向导失败: {str(e)}")

# 获取用户预约记录
@app.route('/api/companion/orders', methods=['GET'])
def get_user_reservations():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        status = request.args.get('status')  # 可选，筛选特定状态的预约
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 构建查询
        query = CompanionReservation.query.filter_by(user_id=openid)
        
        # 按状态筛选
        if status is not None:
            query = query.filter_by(status=int(status))
        
        # 按预约时间倒序排序
        reservations = query.order_by(
            CompanionReservation.created_at.desc()
        ).paginate(
            page=page, per_page=page_size
        )
        
        # 构建返回结果
        result = {
            'total': reservations.total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        for reservation in reservations.items:
            # 获取向导信息
            companion = Companion.query.get(reservation.companion_id)
            companion_info = None
            
            if companion:
                companion_info = {
                    'id': companion.id,
                    'title': companion.title,
                    'avatar': companion.avatar,
                    'price': float(companion.price),
                    'location': companion.location
                }
            
            # 检查用户是否已评价
            has_reviewed = False
            review = CompanionReview.query.filter_by(
                reservation_id=reservation.id,
                user_id=openid
            ).first()
            
            if review:
                has_reviewed = True
            
            # 添加到结果列表
            result['list'].append({
                'id': reservation.id,
                'companion_id': reservation.companion_id,
                'companion_info': companion_info,
                'start_date': reservation.start_date.strftime('%Y-%m-%d'),
                'end_date': reservation.end_date.strftime('%Y-%m-%d'),
                'traveler_count': reservation.traveler_count,
                'special_needs': reservation.special_needs,
                'status': reservation.status,
                'has_reviewed': has_reviewed,
                'created_at': reservation.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取预约记录失败: {e}")
        return make_err_response(f"获取预约记录失败: {str(e)}")

# 发表评价
@app.route('/api/companion/review', methods=['POST'])
def review_companion():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'reservation_id' not in params or 'rating' not in params:
            return make_err_response('缺少必要参数')
        
        reservation_id = params.get('reservation_id')
        rating = float(params.get('rating'))
        content = params.get('content', '')
        images = params.get('images', [])
        
        # 验证评分范围
        if rating < 1 or rating > 5:
            return make_err_response('评分范围应为1-5')
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 检查预约是否存在
        reservation = CompanionReservation.query.get(reservation_id)
        if not reservation:
            return make_err_response('预约不存在')
        
        # 检查预约是否属于当前用户
        if reservation.user_id != openid:
            return make_err_response('无权操作此预约')
        
        # 检查预约状态是否为已完成
        if reservation.status != 2:  # 2表示已完成
            return make_err_response('只能评价已完成的预约')
        
        # 检查是否已经评价过
        existing_review = CompanionReview.query.filter_by(
            reservation_id=reservation_id,
            user_id=openid
        ).first()
        
        if existing_review:
            return make_err_response('已经评价过此预约')
        
        # 处理图片
        images_str = ','.join(images) if images else None
        
        # 创建评价
        review = CompanionReview(
            reservation_id=reservation_id,
            user_id=openid,
            companion_id=reservation.companion_id,
            rating=rating,
            content=content,
            images=images_str
        )
        
        db.session.add(review)
        
        # 更新向导的评分和评价数
        companion = Companion.query.get(reservation.companion_id)
        if companion:
            # 计算新的平均评分
            reviews = CompanionReview.query.filter_by(companion_id=companion.id).all()
            total_rating = sum([r.rating for r in reviews]) + rating
            new_rating = total_rating / (len(reviews) + 1)
            
            companion.rating = new_rating
            companion.review_count += 1
        
        db.session.commit()
        
        # 返回新创建的评价
        result = {
            'id': review.id,
            'reservation_id': review.reservation_id,
            'companion_id': review.companion_id,
            'rating': float(review.rating),
            'content': review.content,
            'images': images,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        db.session.rollback()
        logger.error(f"评价向导失败: {e}")
        return make_err_response(f"评价向导失败: {str(e)}") 