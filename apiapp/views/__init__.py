from flask import request
from flask.json import jsonify


def validate_json():
    if not request.get_json():
        return jsonify({
            'state': 1,
            'msg': '未提供json格式数据'
        })


def validate_params(*param):
    k1 = ','.join(sorted(set(param)))
    k2 = ','.join(sorted(set(request.get_json().keys())))
    if not k1 == k2:
        return jsonify({
            'state': 2,
            'msg': 'POST请求的json数据参数不完整'
        })
