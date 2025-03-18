from flask import jsonify
from wxcloudrun import app, db
import json
import os

@app.route('/api/initialize/status', methods=['GET'])
def initialization_status():
    """获取初始化状态"""
    try:
        # 这里可以检查数据库中是否有初始数据
        from wxcloudrun.model import Attraction
        attraction_count = Attraction.query.count()
        
        if attraction_count > 0:
            return jsonify({
                'code': 0,
                'data': {
                    'initialized': True,
                    'attraction_count': attraction_count
                }
            })
        else:
            return jsonify({
                'code': 0,
                'data': {
                    'initialized': False,
                    'attraction_count': 0
                }
            })
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/initialize/data', methods=['POST'])
def initialize_data():
    """初始化数据"""
    try:
        # 这里可以调用初始化脚本
        # 由于这是一个示例，我们不会真正执行初始化
        # 实际应用中，您可能需要从init_data.py导入相应的函数
        
        return jsonify({
            'code': 0,
            'msg': '数据初始化已触发，请稍后通过status接口查询结果'
        })
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)})

@app.route('/api/initialize/reset', methods=['POST'])
def reset_data():
    """重置数据（危险操作）"""
    try:
        # 清空所有表数据
        # 注意：这是一个危险操作，实际应用中应该加入权限验证
        # 在生产环境中，您可能不希望暴露这样的接口
        
        return jsonify({
            'code': 0,
            'msg': '数据重置已触发，请稍后通过status接口查询结果'
        })
    
    except Exception as e:
        return jsonify({'code': -1, 'msg': str(e)}) 