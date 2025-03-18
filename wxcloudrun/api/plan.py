from flask import request, jsonify
from wxcloudrun import app, db
from wxcloudrun.model import TravelPlan, TravelPlanItem, Attraction
from wxcloudrun.dao import get_user_by_openid
from wxcloudrun.common.response import make_succ_response, make_err_response
import datetime

@app.route('/api/plan/create', methods=['POST'])
def create_plan():
    """创建旅行计划 (从请求头获取openid)"""
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
        title = data.get('title')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        description = data.get('description', '')
        
        if not all([title, start_date, end_date]):
            return jsonify({'code': -1, 'msg': '缺少必要参数'})
        
        # 创建旅行计划
        plan = TravelPlan(
            user_id=user_id,
            title=title,
            start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d').date(),
            end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d').date(),
            description=description
        )
        
        db.session.add(plan)
        db.session.commit()
        
        return jsonify({'code': 0, 'msg': '创建成功', 'data': {'plan_id': plan.id}})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/plan/item/add', methods=['POST'])
def add_plan_item():
    """添加计划项目"""
    try:
        data = request.get_json()
        plan_id = data.get('plan_id')
        day = data.get('day')
        attraction_id = data.get('attraction_id')
        time_period = data.get('time_period', '')
        note = data.get('note', '')
        
        if not all([plan_id, day, attraction_id]):
            return jsonify({'code': -1, 'msg': '缺少必要参数'})
        
        # 检查景点是否存在
        attraction = Attraction.query.get(attraction_id)
        if not attraction:
            return jsonify({'code': -1, 'msg': '景点不存在'})
        
        # 检查计划是否存在
        plan = TravelPlan.query.get(plan_id)
        if not plan:
            return jsonify({'code': -1, 'msg': '旅行计划不存在'})
        
        # 添加计划项目
        item = TravelPlanItem(
            plan_id=plan_id,
            day=day,
            attraction_id=attraction_id,
            time_period=time_period,
            note=note
        )
        
        db.session.add(item)
        db.session.commit()
        
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {'item_id': item.id}})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/plan/list', methods=['GET'])
def get_plans():
    """获取用户的旅行计划列表 (从请求头获取openid)"""
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
        
        plans = TravelPlan.query.filter_by(user_id=user_id).all()
        
        result = {
            'code': 0,
            'data': [
                {
                    'id': plan.id,
                    'title': plan.title,
                    'start_date': plan.start_date.strftime('%Y-%m-%d'),
                    'end_date': plan.end_date.strftime('%Y-%m-%d'),
                    'description': plan.description,
                    'created_at': plan.created_at.strftime('%Y-%m-%d %H:%M:%S')
                } for plan in plans
            ]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/plan/<int:plan_id>', methods=['GET'])
def get_plan_detail(plan_id):
    """获取旅行计划详情 (从请求头获取openid)"""
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
        
        plan = TravelPlan.query.get(plan_id)
        if not plan:
            return jsonify({'code': -1, 'msg': '旅行计划不存在'})
        
        # 验证该计划是否属于当前用户
        if plan.user_id != user_id:
            return jsonify({'code': -1, 'msg': '无权查看该行程'})
        
        # 获取计划项目
        items = TravelPlanItem.query.filter_by(plan_id=plan_id).all()
        
        # 获取景点信息
        attraction_ids = [item.attraction_id for item in items]
        attractions = {a.id: a for a in Attraction.query.filter(Attraction.id.in_(attraction_ids)).all()}
        
        # 构建返回数据
        plan_data = {
            'id': plan.id,
            'title': plan.title,
            'start_date': plan.start_date.strftime('%Y-%m-%d'),
            'end_date': plan.end_date.strftime('%Y-%m-%d'),
            'description': plan.description,
            'created_at': plan.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': []
        }
        
        for item in items:
            item_data = {
                'id': item.id,
                'day': item.day,
                'time_period': item.time_period,
                'note': item.note
            }
            
            attraction = attractions.get(item.attraction_id)
            if attraction:
                item_data['attraction'] = {
                    'id': attraction.id,
                    'name': attraction.name,
                    'cover_image': attraction.cover_image,
                    'address': attraction.address
                }
                
            plan_data['items'].append(item_data)
        
        return jsonify({'code': 0, 'data': plan_data})
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/plans', methods=['GET'])
def get_user_plans():
    """获取用户的旅行计划列表，从请求头获取openid"""
    try:
        # 从请求头获取openid
        openid = request.headers.get('x-wx-openid', '')
        if not openid:
            return make_err_response('缺少用户标识')
        
        # 根据openid查询用户ID
        user = get_user_by_openid(openid)
        if not user:
            return make_err_response('用户不存在')
        
        user_id = user.id
        plans = TravelPlan.query.filter_by(user_id=user_id).all()
        
        result = []
        for plan in plans:
            result.append({
                'id': plan.id,
                'title': plan.title,
                'startDate': plan.start_date.strftime('%Y-%m-%d'),
                'endDate': plan.end_date.strftime('%Y-%m-%d'),
                'description': plan.description,
                'createdAt': plan.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return make_succ_response(result)
    
    except Exception as e:
        return make_err_response(str(e))

@app.route('/api/plans/<int:plan_id>', methods=['GET'])
def get_plan_detail_api(plan_id):
    """获取旅行计划详情，从请求头获取openid"""
    try:
        # 从请求头获取openid
        openid = request.headers.get('x-wx-openid', '')
        if not openid:
            return make_err_response('缺少用户标识')
        
        # 根据openid查询用户ID
        user = get_user_by_openid(openid)
        if not user:
            return make_err_response('用户不存在')
        
        plan = TravelPlan.query.get(plan_id)
        if not plan:
            return make_err_response('旅行计划不存在')
        
        # 验证该计划是否属于当前用户
        if plan.user_id != user.id:
            return make_err_response('无权查看该行程')
        
        # 获取计划项目
        items = TravelPlanItem.query.filter_by(plan_id=plan_id).all()
        
        # 获取景点信息
        attraction_ids = [item.attraction_id for item in items if item.attraction_id]
        attractions = {a.id: a for a in Attraction.query.filter(Attraction.id.in_(attraction_ids)).all()} if attraction_ids else {}
        
        # 构建返回数据
        plan_data = {
            'id': plan.id,
            'title': plan.title,
            'startDate': plan.start_date.strftime('%Y-%m-%d'),
            'endDate': plan.end_date.strftime('%Y-%m-%d'),
            'description': plan.description,
            'createdAt': plan.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': []
        }
        
        for item in items:
            item_data = {
                'id': item.id,
                'day': item.day,
                'timePeriod': item.time_period,
                'note': item.note
            }
            
            if item.attraction_id and item.attraction_id in attractions:
                attraction = attractions[item.attraction_id]
                item_data['attraction'] = {
                    'id': attraction.id,
                    'name': attraction.name,
                    'coverImage': attraction.cover_image,
                    'address': attraction.address
                }
                
            plan_data['items'].append(item_data)
        
        return make_succ_response(plan_data)
    
    except Exception as e:
        return make_err_response(str(e)) 