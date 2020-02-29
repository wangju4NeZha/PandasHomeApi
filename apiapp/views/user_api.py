import hashlib
import uuid
from datetime import datetime

from flask import Blueprint, request, render_template
from flask.json import jsonify
from sqlalchemy import or_, and_, not_

from apiapp.views import validate_json, validate_params
from common import code_, cache_, token_
from db_ import session
from apiapp.models import TUser

blue = Blueprint('user_api', __name__)


@blue.route('/code/', methods=['GET'])
def get_code():
    """
    获取验证码
    :return:
    """
    phone = request.args.get('phone')
    if phone:
        code_.send_code(phone)
        return jsonify({
            'state': 0,
            'msg': '验证码已发送'
        })
    return jsonify({
        'state': 1,
        'msg': '手机号不能为空'
    })


@blue.route('/regist/', methods=['POST'])
def regist():
    """
    注册用户
    :return:
    """
    # 要求JSON数据格式：
    valid_fields = {'name', 'phone', 'code', 'password'}
    data = request.get_json()  # 获取上传的json数据

    if data is None:
        return jsonify({
            'state': 4,
            'msg': '必须提供json格式的数据'
        })
    # 验证前端传入的参数的完整性
    if sorted(set(data.keys())) == sorted(valid_fields):

        # 验证输入的验证码是否正确
        if not code_.valid_code(data['phone'], data['code']):
            return jsonify({
                'state': 2,
                'msg': '验证码输入错误，请确认输入验证码！'
            })
        # 注册信息的填写
        user = TUser()
        user.name = data.get('name')
        user.phone = data.get('phone')
        user.code = data.get('code')
        user.password = data.get('password')
        user.create_time = datetime.now()

        session.add(user)
        session.commit()

        # 向前端返回信息中，包含一个与用户匹配的token（有效事件为一周）
        # 1.基于uuid+user_id生成token
        # 2.将token和user_id保存到缓存（cache_.save_token(token, user_id))
        # JWT单点授权登录
        token = token_.gen_token(user.user_id)
        cache_.add_token(token, user.user_id)
    else:
        return jsonify({
            'state': 1,
            'msg': '参数不完整， 详细请查看接口文档'
        })
    return jsonify({
        'state': 0,
        'msg': '注册成功',
        'token': token
    })


@blue.route('/login/', methods=['POST'])
def login():
    """
    用户登录，每次登录都会生成新的Token
    :return:
    """
    # 验证前端传入的参数是否完整和正确
    resp = validate_json()
    if resp: return resp
    resp = validate_params('phone', 'password')
    if resp: return resp

    # 获取前端发送的请求参数
    data = request.get_json()
    try:
        user = session.query(TUser).filter(or_(TUser.phone == data['phone'],
                                               TUser.name == data['phone']),
                                           TUser.password == data['password']).one()
        if user:
            token = token_.gen_token(user.user_id)
            cache_.add_token(token, user.user_id)

            return jsonify({
                'state': 0,
                'msg': '登录成功',
                'token': token
            })
    except:
        return jsonify({
            'state': 4,
            'msg': '用户名或密码错误',
        })


@blue.route('/modify_auth/', methods=['POST'])
def modify_auth():
    """
    修改密码
    :return:
    """
    # 验证参数完整性
    resp = validate_json()
    if resp: return resp
    resp = validate_params('new_password', 'password', 'token')
    if resp: return resp

    data = request.get_json()
    try:
        # 通过redis获取用户信息
        user_id = cache_.get_user_id(data['token'])
        if not user_id:
            return jsonify({
                'state': 3,
                'msg': '登录已期，需要重新登录并获取新的token',
            })
        # 查询user
        user = session.query(TUser).get(int(user_id))
        if user.password == data['password']:
            user.password = data['new_password']
            session.add(user)
            session.commit()

            return jsonify({
                'state': 0,
                'msg': '修改成功'
            })
        return jsonify({
            'state': 4,
            'msg': '原口令不正确'
        })
    except:
        pass

    return jsonify({
        'state': 3,
        'msg': 'token已无效，尝试重新登录',
    })


@blue.route('/become_superuser/', methods=['GET'])
def become_superuser():
    """
    普通用户升级为会员用户
    :return:
    """
    token = request.args.get('token')
    user_id = cache_.get_user_id(token)
    if user_id:
        user = session.query(TUser).get(user_id==user_id)
        user.is_member = 1
        session.add(user)
        session.commit()
        return jsonify({
            'state': 0,
            'msg': '已成功成为会员用户，您可以开始发布自己的房源了！',
        })
    else:
        return jsonify({
            'state': 1,
            'msg': '未登录， 请先登录！'
        })