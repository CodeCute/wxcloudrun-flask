import json
from flask import Response


def make_succ_empty_response():
    '''
    处理成功返回，不带数据
    :return:
    '''
    data = {
        "code": 0,
        "data": {}
    }
    return Response(json.dumps(data), mimetype='application/json')


def make_succ_response(data):
    '''
    处理成功返回，带数据
    :param data: 数据
    :return:
    '''
    res = {
        "code": 0,
        "data": data
    }
    return Response(json.dumps(res, ensure_ascii=False, default=str), mimetype='application/json')


def make_err_response(err_msg):
    '''
    处理失败返回
    :param err_msg: 错误消息
    :return:
    '''
    res = {
        "code": -1,
        "errorMsg": err_msg
    }
    return Response(json.dumps(res, ensure_ascii=False), mimetype='application/json') 