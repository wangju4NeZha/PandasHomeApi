import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# yyserver1是在 {C:/windows/System32/drivers}/etc/hosts中配置域名
engine = create_engine('mysql+pymysql://root:123456@114.116.245.220:3306/homems')
engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

db_conn = pymysql.Connection(host='114.116.245.220',
                        port=3306,
                        user='root',
                        password='123456',
                        db='homems',
                        charset='utf8',
                        cursorclass=pymysql.cursors.DictCursor)