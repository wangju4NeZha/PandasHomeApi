from flask import Blueprint
from flask import request,jsonify
from sqlalchemy import or_

from apiapp.models import TUser
from apiapp.views import validate_json, validate_params
from common import code_, token_, cache_
from db import session
# from db.models import TUser

blue = Blueprint('user_api',__name__)


@blue.route('/code/',methods=['get'])
def get_code():
    phone = request.args.get('phone')
    if phone:
        code_.send_code(phone)
        return jsonify({
            'state':0,
            'msg':'验证码已发送'
        })
    return jsonify({
        'state': 1,
        'msg': '手机号不能为空'
    })

@blue.route('/regist/', methods=['GET','POST'])
def regist():
    #获取前端传来的JSON格式数据
    valid_fields = {"name","phone","code","password"}
    data = request.get_json()
    if data is None:
        return jsonify({
            'state': 4,
            'msg': '必须提供json格式的参数'
        })

    #验证参数的完整性
    if set(data.keys()) == valid_fields:
        #验证输入的验证码是否正确
        if not code_.valid_code(data['phone'],data['code']):
            return jsonify({
                'state':2,
                'msg':'验证码输入错误，请确认输入的验证码'
            })
        user = TUser()
        user.name = data.get('name')
        user.phone = data.get('phone')
        user.password = data.get('password')

        session.add(user)
        session.commit()
        # 向前端返回信息中，包含一个与用户匹配的token(有效时间为一周)
        # 1. 基于uuid+user_id生成token
        # 2. 将token和user_id保存到缓存（cache_.save_token(token, user_id)）
        # JWT 单点授权登录
        token = token_.gen_token(user.user_id)
        cache_.add_token(token, user.user_id)
    else:
        return jsonify({
            'state': 1,
            'msg': '参数不完整，详情查看接口文档'
        })

    return jsonify({
        'state': 0,
        'msg': '注册成功'
    })

@blue.route('/login/', methods=['POST'])
def login():
    #验证用户是否输入json格式数据
    resp = validate_json()
    if resp: return resp

    #验证用户输入参数是否齐全
    resp = validate_params('phone', 'password')
    if resp: return resp
    data = request.get_json()

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



    return jsonify({
        'state': 4,
        'msg': '用户名或口令输入错误',
    })

@blue.route('/modify_password/',methods=['POST'])
def modify_password():
    #验证用户是否输入json格式数据
    resp = validate_json()
    if resp:return resp

    #验证用户输入参数是否齐全
    resp = validate_params('new_password_str', 'password_str','token')
    if resp: return resp

    data = request.get_json()
    print(data)
    try:
        user_id = cache_.get_user_id(data["token"])
        print(user_id)
        if not user_id:
            return  jsonify({
                'state': 3,
                'msg': '登录已期，需要重新登录并获取新的token',
            })
        user = session.query(TUser).get(int(user_id))
        if user.password == data['password_str']:
            user.password = data['new_password_str']
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

@blue.route('/login_out/')
def login_out():
    pass

@blue.route('/upload_head/',methods=["POST"])
def upload_head():
    #前端上传图片的两种方式(文件上传，base64字符串上传)
    upload_file = request.files.get('head')
    token = request.cookies.get('token')

    user_id = cache_.get_user_id(token)
    file_name = upload_file.filename

    return jsonify({
        'state':0,
        'msg':'上传成功'
    })


