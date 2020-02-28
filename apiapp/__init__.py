from flask import Flask

import settings
from flask_cors import CORS

app = Flask(__name__,static_folder=settings.STATIC_DIR,
            static_url_path='/s/')

app.config['ENV'] = 'developement' #开发模式
app.config['DEBUG'] = True

CORS(app)  # 全局方式支持跨域请求（前端服务器和后端API服务器分开部署）


