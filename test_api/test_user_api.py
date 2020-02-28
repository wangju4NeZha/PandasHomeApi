import requests

from unittest import TestCase

HOST = 'localhost'
PORT = 5000

base_url = f'http://{HOST}:{PORT}'

data = {
    'phone': '18526081087',
    # 'token': 'aa7dcc99349626f524b4e7676493ef87'
}

class TestUserApi(TestCase):
    def test_a_send_code(self):
        url = base_url+f'/api/code/?phone={data["phone"]}'
        resp = requests.get(url)
        print(resp.json())

    def test_b_regist(self):
        url = base_url + '/api/regist/'
        resp = requests.post(url, json={
            'name': 'xiangshu',
            'phone': data['phone'],
            'code': '3408',
            'password': '123456'  # 密文要求（前端）：需要使用hash算法
        })
        print(resp.json())

    def test_c_login(self):
        url = base_url + '/api/login/'
        resp = requests.post(url,json={
            'phone':data['phone'],
            'password':'123456'
        })
        resp_data = resp.json()
        print(resp_data)
        if resp_data['state'] == 0:
            data['token'] = resp_data['token']

    def test_d_login(self):
        url = base_url + '/api/modify_password/'
        resp = requests.post(url, json={
            'token': data['token'],
            'password_str': '123458',
            'new_password_str': '123456',
        })
        resp_data = resp.json()
        print(resp_data)