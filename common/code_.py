import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from common import cache_


def send_code(phone):
    # 1.生成code
    code_set = list()
    while len(code_set) < 4:
        code_set.append(str(random.randint(0, 9)))
    code = ''.join(code_set)
    # 2.保存code数据库 - redis
    cache_.save_code(phone, code)
    # 3.获取短信
    client = AcsClient('LTAI4FqbMxbMPrnKSBsu5KSh', 'copeGy6ElAJ0fdleAkYxcOME5TR4CJ', 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "熊猫之家")
    request.add_query_param('TemplateCode', "SMS_184210172")
    request.add_query_param('TemplateParam', '{"code":"%s"}' % code)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    print(str(response, encoding='utf-8'))


def valid_code(phone, code):
    # 1.从缓存中获取phone中的code（发送的code）
    code_cache = cache_.get_code(phone)
    # 2.判断code(输入)和缓存中的code是否相同
    return code == code_cache


if __name__ == '__main__':
    send_code("15829377201")
