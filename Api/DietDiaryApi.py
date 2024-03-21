from flask_restful import Resource, fields, marshal_with, request
from models import DietDiary


class DietDiaryApi(Resource):
    # 定义要返回的字段
    resource_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'meals': fields.String,
        'views': fields.Integer,
        'created_time': fields.Integer,
    }

    @marshal_with(resource_fields)
    def get(self):
        """
        返回所有记录
        :return:
        """
        # 查询数据库
        diet_diary = DietDiary.query.all()
        return diet_diary

    # /diet_diary?user_id=1
    @marshal_with(resource_fields)
    def get(self):
        """
        返回所有记录
        :return:
        """
        user_id = request.args.get('user_id')
        diet_diary = DietDiary.query.filter(DietDiary.user_id == user_id).all()
        return diet_diary
