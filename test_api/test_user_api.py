import requests

from unittest import TestCase

from common import cache_, rd

HOST = 'localhost'
PORT = 5000

base_url = f'http://{HOST}:{PORT}'

data = {
    'phone': '15829377201',
    'token': 'abacab33b10b0539d898f265c6c119fa',
}


class TestUserApi(TestCase):
    # 发送验证码
    def test_a_send_code(self):
        url = base_url + '/api/code/?phone=%s' % data['phone']
        resp = requests.get(url)
        print(resp.json())

    # 注册
    def test_b_regist(self):
        url = base_url + '/api/regist/'
        resp = requests.post(url, json={
            'name': 'zhagnsan',
            'phone': data['phone'],
            'code': '8070',  #
            'password': '123456'  # 密文要求（前端）： 需要使用hash算法
        })
        print(resp.json())

    # 登录
    def test_c_login(self):
        url = base_url + '/api/login/'
        resp = requests.post(url, json={
            'phone': data['phone'],
            'password': '123456'
        })
        resp_data = resp.json()
        print(resp_data)
        if resp_data['state'] == 0:
            data['token'] = resp_data['token']

    # 改密码
    def test_d_modify_auth(self):
        url = base_url + '/api/modify_auth/'
        resp = requests.post(url, json={
            'new_password': '45678',
            'password': '123456',
            'token': data['token']
        })
        resp_data = resp.json()
        print(resp_data)

    # 发布房源
    def test_e_add_house(self):
        url = base_url + '/api/add/'
        print(url)

        resp = requests.post(url, json={
            'image': '2.jpg',
            'name': 'wangzhai',
            'type': '别墅',
            'address': '我家',
            'price': '666',
            'area': '8888',
            'description': 'daa',
            'token': 'abacab33b10b0539d898f265c6c119fa'
        })
        resp_data = resp.json()
        print(resp_data)

    # 删除房源
    def test_f_del_house(self):
        url = base_url + '/api/del_house/'
        print(url)

        resp = requests.post(url, json={
            'house_id': 2,
            'token': 'abacab33b10b0539d898f265c6c119fa'
        })
        print(resp.json())

    # 改变出售状态
    # def test_g_change_sale_state(self):
    #     url = base_url + '/api/change_sale_state/'
    #     print(url)
    #
    #     resp = requests.post(url, json={
    #         'house_id': 2,
    #         'token': 'abacab33b10b0539d898f265c6c119fa'
    #     })
    #     print(resp.json())

    # 修改房源信息
    def test_h_change_house_info(self):
        url = base_url + '/api/change_house_info/'
        print(url)

        resp = requests.post(url, json={
            'image': '1.jpg',
            'name': 'yueliang',
            'type': 'xingqiu',
            'address': '我家',
            'price': '999',
            'area': '8888',
            'description': '擦擦',
            'token': 'abacab33b10b0539d898f265c6c119fa',
            'house_id': 2,
        })
        print(resp.json())

    # 查询所登录房东的房源
    def test_k_list_user_houses(self):
        token = 'abacab33b10b0539d898f265c6c119fa'
        url = base_url + '/api/list_houses/?token=' + token
        resp = requests.get(url)
        print(resp.json())

    # 列出所有房源
    def test_l_list_all_houses(self):
        url = base_url + '/api/list_all_houses/'
        resp = requests.get(url)
        print(resp.json())

    # 房源详情（包含审核）
    def test_m_house_detail_info(self):
        url = base_url + '/api/detail/?house_id=2&token=abacab33b10b0539d898f265c6c119fa'
        print(url)
        resp = requests.get(url)
        print(resp.json())

    # 普通用户升级为会员用户
    def test_n_become_superuser(self):
        url = base_url + '/api/become_superuser/?token=abacab33b10b0539d898f265c6c119fa'
        resp = requests.get(url)
        print(resp.json())
