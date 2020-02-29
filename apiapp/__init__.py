from flask import Flask
from flask_cors import CORS

import settings
from apiapp.views import user_api, house_api


app = Flask(__name__,
            static_folder=settings.STATIC_DIR,
            static_url_path='/s/')

app.config['ENV'] = 'development'  # production
app.config['DEBUG'] = True

app.register_blueprint(user_api.blue, url_prefix='/api/')
app.register_blueprint(house_api.blue, url_prefix='/api/')
CORS(app)  # 全局方式支持跨域请求（前端服务器和后端API服务器分开部署）
