import json
from datetime import datetime

from flask import request, Response, stream_with_context
from flask_restful import Resource, fields, marshal_with
from zhipuai import ZhipuAI
import jwt
from exts import db
from models import DietDiary, User, UserInfo

API_KEY = "e4a1396cddb0df3a16c9def68e292555.iW5H7PmF1l5nbDMn"
MODEL_NAME = "glm-4"
JWT_SECRET = "0657869022fb9353da65533dea1beb38"


# 使用流式传输生成响应的函数
def generate_stream(diary):
    client = ZhipuAI(api_key=API_KEY)
    if diary == "":
        return
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user",
                 "content": '''
                 您好，作为饮食分析师，请您使用中文分析以下用户的基本信息和他们的饮食日记。您需要提供该用户的饮食信息以及未来几天的饮食推荐。为了确保分析的准确性和安全性，请务必不要提供任何个人敏感信息。所有分析应基于用户提供的信息进行，同时，请确保您的建议是基于一般性的营养知识和用户的健康状况，而非具体个人情况。
                '''},
                {"role": "user", "content": diary},
            ],
            stream=True,
            # temperature=0.5,
        )
    except Exception as e:
        print(e)
        return
    for chunk in response:
        # 将每个chunk转换为JSON字符串，并附加一个换行符以分隔数据块
        yield chunk.choices[0].delta.content


class AnalyseStream(Resource):
    def get(self):
        header_jwt = request.headers.get("Authorization")
        decoded_jwt = jwt.decode(header_jwt, JWT_SECRET, algorithms=['HS256'])
        if decoded_jwt['user_id'] is None:
            return Response("user_id is required", content_type="text/event-stream")
        user_id = decoded_jwt['user_id']
        # 获取用户信息
        user = db.session.query(User).filter(User.id == user_id).first()
        if user is None:
            return Response("用户不存在", content_type="text/event-stream")

        user_info = db.session.query(UserInfo).filter(UserInfo.id == user_id).first()

        # 从数据获取用户的前七天的饮食日记
        diet_diary = db.session.query(DietDiary).filter(DietDiary.user_id == user_id).order_by(
            DietDiary.created_time.desc()).limit(7)
        # 生成用户的饮食日记
        if diet_diary.count() == 0:
            return Response("用户没有饮食日记", content_type="text/event-stream")
        diary = ""
        diary += "用户信息\n"
        diary += "姓名：" + user.nickname + "\n"
        diary += "年龄：" + str(datetime.now().year - datetime.fromtimestamp(user_info.birth_date).year) + "\n"
        diary += "性别：" + user_info.gender + "\n"
        diary += "体重：" + str(user_info.weight) + "kg\n"
        diary += "身高：" + str(user_info.height) + "cm\n"
        diary += "健康状况" + str(user_info.health_conditions) + "\n"
        diary += "饮食日记\n"
        for diary_item in diet_diary:
            # 将数字类型秒级时间戳created_time格式化为YYYY-MM-DD
            created_time = datetime.fromtimestamp(diary_item.created_time)
            diary += created_time.strftime("%Y-%m-%d") + "\n"
            diary += diary_item.meals + "\n"
        # print(diary)
        return Response(stream_with_context(generate_stream(diary)), content_type="text/event-stream")
