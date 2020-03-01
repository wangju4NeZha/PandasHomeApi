import requests

from unittest import TestCase

HOST = 'localhost'
PORT = 5000

base_url = f'http://{HOST}:{PORT}'

data = {
    'phone': '18526081087',
    'token': 'a8b3a7fd871e4e2e90d91d3fc0fe1158'
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
            'code': '649730',
            'password': '123456'  # 密文要求（前端）：需要使用hash算法
        })
        print(resp.json())

    def test_c_login(self):
        url = base_url + '/api/login/'
        resp = requests.post(url,json={
            'phone':data['phone'],
            'password':'123458'
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

    def test_e_upload_head(self):
        url = base_url+"/api/upload_head/"
        resp = requests.post(url, files={
            'head': ('tiger.jpg', open('tiger.jpg', 'rb'), 'image/jpeg')
        }, cookies={'token': data['token']})

        print(resp.json())

    def test_f_login_out(self):
        url = base_url+"/api/login_out/"
        resp = requests.get(url,cookies={'token':data['token']})

        print(resp.json())

    def test_g_detail_resource(self):
        url = base_url + "/api/detail_resource/"
        resp = requests.get(url, json={

        },cookies={'token': data['token']})

        print(resp.json())


    def test_h_get_resource(self):
        url = base_url+"/api/get_resource/"
        resp = requests.get(url,cookies={'token':data['token']})

        print(resp.json())

    def test_i_integral(self):
        url = base_url + "/api/integral/"
        resp = requests.get(url, cookies={'token': data['token']})

        print(resp.json())

    def test_j_about_pandas(self):
        url = base_url + "/api/about_pandas/"
        resp = requests.get(url)

        print(resp.json())