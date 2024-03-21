# config.py
USERNAME = 'root'
PASSWORD = 'root'
HOSTNAME = "127.0.0.1"
PORT = '3307'
DATABASE = 'healthy_system'

DIALECT = 'mysql'
DRIVER = 'pymysql'

# 连接数据的URI
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

SWAGGER_TITLE = "API"
SWAGGER_DESC = "API接口"
# 地址，必须带上端口号
SWAGGER_HOST = "localhost:5000"

API_KEY = "e4a1396cddb0df3a16c9def68e292555.iW5H7PmF1l5nbDMn"