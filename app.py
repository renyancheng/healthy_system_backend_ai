import time

from flask import Flask, request, Response, stream_with_context
from flask_restful import Api, Resource
import config
from exts import db
from Api.DietDiaryApi import DietDiaryApi
from Api.AnalyseStream import AnalyseStream

app = Flask(__name__)

# 设置 Flask-JWT-Extended 扩展

api = Api(app)
# 加载配置文件
app.config.from_object(config)
# db绑定app
db.init_app(app)

api.add_resource(AnalyseStream, '/analyse_stream')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
