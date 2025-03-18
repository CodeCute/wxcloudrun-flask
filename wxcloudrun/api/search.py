from flask import request
from run import app
import logging
from wxcloudrun.model import Attraction, News, Companion, Solution
from wxcloudrun import db
from wxcloudrun.response import make_succ_response, make_err_response
from sqlalchemy import or_

# 配置日志
logger = logging.getLogger('travel-cloud')

# 综合搜索API
@app.route('/api/search', methods=['GET'])
def search():
    try:
        keyword = request.args.get('keyword', '')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        search_type = request.args.get('type', 'all')  # 可选值: all, attraction, news, companion, solution
        
        if not keyword:
            return make_err_response('搜索关键词不能为空')
        
        # 初始化结果
        result = {
            'keyword': keyword,
            'page': page,
            'page_size': page_size,
            'type': search_type,
            'total': 0,
            'attractions': [],
            'news': [],
            'companions': [],
            'solutions': []
        }
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 根据搜索类型执行不同的查询
        if search_type == 'all' or search_type == 'attraction':
            # 搜索景点
            attractions = Attraction.query.filter(
                or_(
                    Attraction.name.like(f'%{keyword}%'),
                    Attraction.description.like(f'%{keyword}%'),
                    Attraction.address.like(f'%{keyword}%')
                )
            ).limit(page_size if search_type != 'all' else page_size // 4).offset(offset if search_type != 'all' else 0).all()
            
            for attraction in attractions:
                result['attractions'].append({
                    'id': attraction.id,
                    'name': attraction.name,
                    'cover_image': attraction.cover_image,
                    'address': attraction.address,
                    'price': attraction.price,
                    'type': 'attraction'
                })
        
        if search_type == 'all' or search_type == 'news':
            # 搜索资讯
            news_list = News.query.filter(
                or_(
                    News.title.like(f'%{keyword}%'),
                    News.content.like(f'%{keyword}%')
                )
            ).limit(page_size if search_type != 'all' else page_size // 4).offset(offset if search_type != 'all' else 0).all()
            
            for news in news_list:
                result['news'].append({
                    'id': news.id,
                    'title': news.title,
                    'cover_image': news.cover_image,
                    'view_count': news.view_count,
                    'like_count': news.like_count,
                    'created_at': news.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'type': 'news'
                })
        
        if search_type == 'all' or search_type == 'companion':
            # 搜索向导
            companions = Companion.query.filter(
                or_(
                    Companion.title.like(f'%{keyword}%'),
                    Companion.description.like(f'%{keyword}%'),
                    Companion.location.like(f'%{keyword}%')
                )
            ).limit(page_size if search_type != 'all' else page_size // 4).offset(offset if search_type != 'all' else 0).all()
            
            for companion in companions:
                result['companions'].append({
                    'id': companion.id,
                    'title': companion.title,
                    'avatar': companion.avatar,
                    'cover_image': companion.cover_image,
                    'price': float(companion.price),
                    'location': companion.location,
                    'rating': float(companion.rating),
                    'type': 'companion'
                })
        
        if search_type == 'all' or search_type == 'solution':
            # 搜索解决方案
            solutions = Solution.query.filter(
                or_(
                    Solution.title.like(f'%{keyword}%'),
                    Solution.description.like(f'%{keyword}%'),
                    Solution.content.like(f'%{keyword}%')
                )
            ).limit(page_size if search_type != 'all' else page_size // 4).offset(offset if search_type != 'all' else 0).all()
            
            for solution in solutions:
                result['solutions'].append({
                    'id': solution.id,
                    'title': solution.title,
                    'cover_image': solution.cover_image,
                    'duration': solution.duration,
                    'price_estimate': float(solution.price_estimate) if solution.price_estimate else None,
                    'difficulty': solution.difficulty,
                    'type': 'solution'
                })
        
        # 计算总数
        if search_type == 'attraction':
            result['total'] = Attraction.query.filter(
                or_(
                    Attraction.name.like(f'%{keyword}%'),
                    Attraction.description.like(f'%{keyword}%'),
                    Attraction.address.like(f'%{keyword}%')
                )
            ).count()
        elif search_type == 'news':
            result['total'] = News.query.filter(
                or_(
                    News.title.like(f'%{keyword}%'),
                    News.content.like(f'%{keyword}%')
                )
            ).count()
        elif search_type == 'companion':
            result['total'] = Companion.query.filter(
                or_(
                    Companion.title.like(f'%{keyword}%'),
                    Companion.description.like(f'%{keyword}%'),
                    Companion.location.like(f'%{keyword}%')
                )
            ).count()
        elif search_type == 'solution':
            result['total'] = Solution.query.filter(
                or_(
                    Solution.title.like(f'%{keyword}%'),
                    Solution.description.like(f'%{keyword}%'),
                    Solution.content.like(f'%{keyword}%')
                )
            ).count()
        else:
            # 全部类型的总数
            result['total'] = len(result['attractions']) + len(result['news']) + len(result['companions']) + len(result['solutions'])
        
        return make_succ_response(result)
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        return make_err_response(f"搜索失败: {str(e)}") 