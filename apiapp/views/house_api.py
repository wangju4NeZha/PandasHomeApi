from flask import Blueprint, request, g, redirect, url_for
from flask.json import jsonify

from apiapp.views import validate_json, validate_params
from common import cache_
from common.serializer import to_json
from db_ import session
from apiapp.models import TUser, THouse, THouseVerify

blue = Blueprint('house_api', __name__)


@blue.route('/add/', methods=['POST'])
def add_house():
    # 验证参数完整性
    resp = validate_json()
    if resp: return resp
    resp = validate_params('image', 'name', 'type', 'address', 'price', 'area', 'description', 'token')
    if resp: return resp

    house_info = request.get_json()
    user_id = cache_.get_user_id(house_info['token'])
    house = THouse()
    house.user_id = user_id
    house.image = house_info['image']
    house.name = house_info['name']
    house.type = house_info['type']
    house.address = house_info['address']
    house.price = house_info['price']
    house.area = house_info['area']
    house.description = house_info['description']

    session.add(house)
    session.commit()
    return jsonify({
        'state': '发布房源成功',
        'data': house_info
    })


@blue.route('/del_house/', methods=['POST'])
def del_house():
    """
    删除房源信息的房源信息
    :return:
    """
    # 验证参数完整性
    resp = validate_json()
    if resp: return resp
    resp = validate_params('token', 'house_id')
    if resp: return resp

    data = request.get_json()
    house_id = data['house_id']
    token = data['token']
    user_id = cache_.get_user_id(token)
    house = session.query(THouse).filter(house_id == house_id, user_id == user_id)
    print(house)
    if house:
        obj = house.first()
        obj.is_public = 1
        session.add(obj)
        session.commit()
        return jsonify({
            'state': 0,
            'msg': '删除成功'
        })
    else:
        return jsonify({
            'state': 1,
            'msg': '登录已过期或房屋信息已删除'
        })


@blue.route('/change_house_info/', methods=['POST'])
def change_house_info():
    """
    改变房屋信息
    :return:
    """
    resp = validate_json()
    if resp: return resp
    resp = validate_params('image', 'name', 'type', 'address', 'price', 'area', 'description', 'token', 'house_id')
    if resp: return resp

    data = request.get_json()
    house_id = data['house_id']
    token = data['token']
    user_id = cache_.get_user_id(token)
    if user_id:
        house = session.query(THouse).filter(house_id == house_id, user_id == user_id).first()
        house.is_public = 1
        house.image = data['image']
        house.name = data['name']
        house.type = data['type']
        house.address = data['address']
        house.price = data['price']
        house.area = data['area']
        house.description = data['description']

        session.add(house)
        session.commit()
        return jsonify({
            'state': 0,
            'msg': '房源信息修改成功！'
        })
    else:
        return jsonify({
            'state': 1,
            'msg': '还未登陆，请先登录！'
        })


@blue.route('/list_houses/', methods=['GET'])
def list_user_houses():
    """
    查看现登录房东的房源信息
    :return:
    """
    data = request.args.get('token')
    user_id = cache_.get_user_id(data)
    if user_id:
        ret = session.query(THouse).filter(THouse.user_id == user_id).all()
        return jsonify({
            'state': 0,
            'msg': '查询成功',
            'data': to_json(ret)
        })
    else:
        return jsonify({
            'state': 1,
            'msg': '未登录'
        })


@blue.route('/list_all_houses/', methods=['GET'])
def list_all_houses():
    """
    查看所有房源详细信息
    :return:
    """
    ret = session.query(THouse).all()
    return jsonify({
        'state': 0,
        'data': to_json(ret)
    })


@blue.route('/detail/', methods=['GET'])
def detail_info():
    """
    查看房屋的详情
    :return:
    """
    token = request.args.get('token')
    user_id = cache_.get_user_id(token)
    if user_id:
        house_id = request.args.get('house_id')

        verify_info = session.query(THouseVerify).filter(THouseVerify.house_id == house_id)
        if verify_info:
            obj = verify_info.first()
            return jsonify({
                'state': 0,
                'msg': '查询成功',
                'data': {
                    'verify_state': obj.verify_status,
                    'house': to_json(obj.house)
                }
            })
        else:
            return jsonify({
                'state': 2,
                'msg': '查询失败，发生了未知错误，请重新尝试！'
            })

    return jsonify({
        'state': 1,
        'msg': '未登录，请先登录！'
    })
