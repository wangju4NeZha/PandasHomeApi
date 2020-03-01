import os

from flask import Blueprint, Response
from flask import request,jsonify
from sqlalchemy import or_

import settings
from apiapp.models import TUser, TScore, TPanda, Contract
from apiapp.views import validate_json, validate_params
from common import code_, token_, cache_, oss_
from db import session
# from db.models import TUser
from db.raw import query

blue = Blueprint('user_api',__name__)

#发送短信验证码
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

#用户注册
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

#用户登陆
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

        head_url = ''
        if user.img:
            head_url = cache_.get_head_url(user.img)
            if not head_url:
                head_url = oss_.get_oss_img_url(user.img)

                cache_.save_head_url(user.img, head_url)
        resp:Response =  jsonify({
            'state': 0,
            'msg': '登录成功',
            'token': token
        })
        # 设置响应对象的cookie，向客户端响应cookie
        resp.set_cookie('token', token)
        resp.set_cookie('head', head_url)
        return resp

    return jsonify({
        'state': 4,
        'msg': '用户名或口令输入错误',
    })

#用户修改密码
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

#用户注销
@blue.route('/login_out/')
def login_out():
    token = request.cookies.get('token')
    cache_.del_token(token)

    return jsonify({
        'state':0,
        'msg':'退出登陆成功'
    })

#用户上传头像
@blue.route('/upload_head/',methods=["POST"])
def upload_head():
    #前端上传图片的两种方式(文件上传，base64字符串上传)
    upload_file = request.files.get('head')
    token = request.cookies.get('token')

    user_id = cache_.get_user_id(token)
    file_name = upload_file.filename

    save_file_path = os.path.join(settings.TEMP_DIR, file_name)
    # 保存上传的文件到临时的目录中
    upload_file.save(save_file_path)

    # 将临时的文件上传到oss服务器中， 并获取到缩小后的图片URL
    head_url = oss_.upload_head(user_id, file_name, save_file_path)

    # 将head_url保存到用户的表中
    user = session.query(TUser).get(user_id)
    user.img = f'{user_id}-{file_name}'  # 存储oss上的key对象
    session.add(user)
    session.commit()

    # 将头像的URL 存到 redis中
    cache_.save_head_url(user.img, head_url)

    # 删除临时的文件
    os.remove(save_file_path)

    return jsonify({
        'state':0,
        'msg':'上传成功',
        'head':head_url
    })

@blue.route('/head/', methods=["GET"])
def get_head():
    token = request.cookies.get('token')  # 1. 从请求参数中获取  2. 从请求头的Cookie中获取

    user_id = cache_.get_user_id(token)

    user = session.query(TUser).get(user_id)

    head_url = cache_.get_head_url(user.img)
    if not head_url:
        head_url = oss_.get_oss_img_url(user.img)
        cache_.save_head_url(user.img, head_url)

    return jsonify({
        'state': 0,
        'head': head_url
    })

#用户更新信息
@blue.route('/detail_resouce/',methods=["POST"])
def detail_resouce():
    # 验证用户是否输入json格式数据
    resp = validate_json()
    if resp: return resp

    # 验证用户输入参数是否齐全
    resp = validate_params('sex', 'nickname','nickname','identity_number')
    if resp: return resp
    data = request.get_json()
    print(data)

    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })

    #根据id查询用户
    user = session.query(TUser).get(user_id)
    user.sex = data["sex"]
    user.nickname = data["nickname"]
    user.email = data["email"]
    user.identity_number = data["identity_number"]
    session.add(user)
    session.commit()

    return jsonify({
        'state':0,
        'msg':'更新信息成功'
    })

#获取用户详细资料
@blue.route('/get_resource/',methods=["GET"])
def get_resource():
    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })

    # 根据id查询用户
    user = session.query(TUser).get(user_id)
    print(user)

    return jsonify({
        'state':0,
        'msg':'ok',
        'name':user.name,
        'sex':user.sex,
        'nickname':user.nickname,
        'email':user.email,
        'phone':user.phone,
        'identity_number':user.identity_number

    })

#用户积分查询
@blue.route('/integral/',methods=["GET"])
def interal():
    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })
    sql = 'select score from t_score join t_user on t_score.user_id=t_user.user_id where t_score.user_id=%s'
    score = query(sql,user_id)
    return jsonify({
        'state':0,
        'msg':'ok',
        'interal':score[0]['score']
    })


#关于我们
@blue.route('/about_pandas/',methods=["GET"])
def about_pandas():
    sql = 'select detail_content from t_panda where t_panda.panda_id=%s'
    detail = query(sql, 1)

    return jsonify({
        'state': 0,
        'msg': 'ok',
        'interal': detail[0]['detail_content']
    })

#用户提交租房合同

@blue.route('/provide_contract/',methods=["POST"])
def contract():
    # 验证用户是否输入json格式数据
    resp = validate_json()
    if resp: return resp

    # 验证用户输入参数是否齐全
    resp = validate_params('start_time', 'stoptime', 'content')
    if resp: return resp
    data = request.get_json()

    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })

    # 根据id查询用户
    cont = session.query(Contract).filter(user_id)
    cont.start_time = data['start_time']
    cont.stop_time = data['stop_time']
    cont.content = data['content']

    session.add(cont)
    session.commit()
    return jsonify({
        'state':0,
        'msg':'合同添加完成'
    })

#查看合同
@blue.route('/get_contract/',methods=["GET"])
def get_contract():
    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })
    sql = 'select start_time,stop_time,content from t_user join contract c2 on t_user.user_id = c2.user_id where c2.user_id=%s'
    cont_detail = query(sql,user_id)
    return jsonify({
            'state': 0,
            'msg': '已查询到合同信息',
            'start_time':cont_detail[0]["start_time"],
            'stop_time': cont_detail[0]["stop_time"],
            'content': cont_detail[0]["content"]
        })

#查看房屋交易记录
@blue.route('/traderecord/',methods=["GET"])
def traderecord():
    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })
    sql = 'select th.name,th.img,td.payment_date,td.payment_type from t_house th,t_tradingrecord td,t_user tu where th.user_id=td.user_id and td.user_id=tu.user_id and td.user_id=%s'
    house_detail = query(sql, user_id)
    return jsonify({
        'state': 0,
        'msg': '已查询到房屋交记录',
        'housename': house_detail[0]["name"],
        'houseimg': house_detail[0]["img"],
        'payment_date': house_detail[0]["payment_date"],
        'payment_type':house_detail[0]["payment_type"]
    })

@blue.route('/get_order/',methods=["GET"])
def get_order():
    token = request.cookies.get('token')
    user_id = cache_.get_user_id(token)
    if not user_id:
        return jsonify({
            'state': 3,
            'msg': '登录已期，需要重新登录并获取新的token',
        })

    #1查看全部订单
    sql = 'select td.* from t_user tu join t_order td on tu.user_id = td.user_id where td.order_status=%s'
    all_order = query(sql,0)
    return jsonify({
        'state':0,
        'msg':'全部订单信息',
        'order':all_order
    })
    #2.查看已支付订单
    sql = 'select td.* from t_user tu join t_order td on tu.user_id = td.user_id where td.order_status=%s'
    pay_order = query(sql, 1)
    return jsonify({
        'state': 0,
        'msg': '已支付订单信息',
        'order': pay_order
    })
    #3.查看待支付订单
    sql = 'select td.* from t_user tu join t_order td on tu.user_id = td.user_id where td.order_status=%s'
    nopay_order = query(sql, 2)
    return jsonify({
        'state': 0,
        'msg': '待支付订单信息',
        'order': nopay_order
    })










