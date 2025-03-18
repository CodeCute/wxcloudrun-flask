from flask import request
from run import app
import logging
from wxcloudrun.model import Solution, SolutionApplication, TravelPlan
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

# 获取解决方案列表
@app.route('/api/solution/list', methods=['GET'])
def get_solution_list():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        duration = request.args.get('duration')  # 可选，按天数筛选
        difficulty = request.args.get('difficulty')  # 可选，按难度筛选
        
        # 构建查询
        query = Solution.query
        
        # 应用筛选条件
        if duration:
            query = query.filter_by(duration=int(duration))
        
        if difficulty:
            query = query.filter_by(difficulty=int(difficulty))
        
        # 按查看次数排序
        solutions = query.order_by(
            Solution.view_count.desc()
        ).paginate(
            page=page, per_page=page_size
        )
        
        # 构建返回结果
        result = {
            'total': solutions.total,
            'page': page,
            'page_size': page_size,
            'list': []
        }
        
        for solution in solutions.items:
            result['list'].append({
                'id': solution.id,
                'title': solution.title,
                'description': solution.description,
                'cover_image': solution.cover_image,
                'duration': solution.duration,
                'price_estimate': float(solution.price_estimate) if solution.price_estimate else None,
                'difficulty': solution.difficulty,
                'view_count': solution.view_count,
                'apply_count': solution.apply_count,
                'created_at': solution.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取解决方案列表失败: {e}")
        return make_err_response(f"获取解决方案列表失败: {str(e)}")

# 获取解决方案详情
@app.route('/api/solution/<int:solution_id>', methods=['GET'])
def get_solution_detail(solution_id):
    try:
        solution = Solution.query.get(solution_id)
        if not solution:
            return make_err_response('解决方案不存在')
        
        # 增加浏览次数
        solution.view_count += 1
        db.session.commit()
        
        # 构建返回数据
        result = {
            'id': solution.id,
            'title': solution.title,
            'description': solution.description,
            'cover_image': solution.cover_image,
            'content': solution.content,
            'duration': solution.duration,
            'price_estimate': float(solution.price_estimate) if solution.price_estimate else None,
            'difficulty': solution.difficulty,
            'view_count': solution.view_count,
            'apply_count': solution.apply_count,
            'created_at': solution.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': solution.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"获取解决方案详情失败: {e}")
        return make_err_response(f"获取解决方案详情失败: {str(e)}")

# 应用解决方案到行程
@app.route('/api/solution/apply', methods=['POST'])
def apply_solution():
    try:
        # 获取请求体参数
        params = request.get_json()
        if not params or 'solution_id' not in params:
            return make_err_response('缺少必要参数')
        
        solution_id = params.get('solution_id')
        travel_date = params.get('travel_date')
        notes = params.get('notes')
        
        # 获取用户openid
        openid = get_openid()
        if not openid:
            return make_err_response('未登录或登录已过期')
        
        # 检查解决方案是否存在
        solution = Solution.query.get(solution_id)
        if not solution:
            return make_err_response('解决方案不存在')
        
        # 处理日期
        travel_date_obj = None
        if travel_date:
            try:
                travel_date_obj = datetime.strptime(travel_date, '%Y-%m-%d').date()
            except ValueError:
                return make_err_response('日期格式不正确，应为YYYY-MM-DD')
        
        # 创建应用记录
        application = SolutionApplication(
            solution_id=solution_id,
            user_id=openid,
            travel_date=travel_date_obj,
            notes=notes
        )
        
        db.session.add(application)
        
        # 更新解决方案的应用次数
        solution.apply_count += 1
        
        # 如果提供了旅行日期，可以创建行程计划
        if travel_date_obj:
            # 创建行程
            travel_plan = TravelPlan(
                user_id=openid,
                title=f'基于{solution.title}的行程',
                start_date=travel_date_obj,
                end_date=travel_date_obj + datetime.timedelta(days=solution.duration - 1) if solution.duration else None,
                description=f'从{solution.title}生成的行程计划'
            )
            
            db.session.add(travel_plan)
            
            # 提交以获取travel_plan.id
            db.session.flush()
            
            # 可以在这里添加行程项目的生成逻辑，这需要解析solution.content的内容
            # 由于解决方案的内容结构可能比较复杂，这里简化处理
            
            # 返回行程信息
            application.plan_id = travel_plan.id
        
        db.session.commit()
        
        # 构建返回数据
        result = {
            'id': application.id,
            'solution_id': application.solution_id,
            'travel_date': application.travel_date.strftime('%Y-%m-%d') if application.travel_date else None,
            'notes': application.notes,
            'created_at': application.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return make_succ_response(result)
    except Exception as e:
        db.session.rollback()
        logger.error(f"应用解决方案失败: {e}")
        return make_err_response(f"应用解决方案失败: {str(e)}") 