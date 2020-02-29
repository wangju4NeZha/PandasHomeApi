import random

from flask import g, request, url_for


def load_middleware(app):

    if request.path == url_for('user_api.login'):
        @app.before_first_request
        def a():
            print("before_first_request......")

        @app.before_request
        def b():
            print("before_request......")
            num = random.randint(1,100)
            if num >= 80:
                g.book = "《十万个为什么》"   # 动态给g对象添加一个book属性
                return "<h3>恭喜，你中奖了，中奖号为：<span style='color:red'>" + str(num) + "</span></h3>"

            g.book = "《芸芸众生》"

        @app.after_request
        def c(response):    #  由after_request装饰器装饰的函数必须接收一个响应对象
            print("after_request......,g.book=",g.book)
            return response  # 一定要返回该响应对象

        @app.teardown_request
        def d(e):
            print("teardown_request,异常对象为：",e)

