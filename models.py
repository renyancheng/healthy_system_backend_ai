from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.BigInteger, nullable=False)
    updated_time = db.Column(db.BigInteger, nullable=False)
    last_login_time = db.Column(db.BigInteger, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    birth_date = db.Column(db.BigInteger, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    activity_level = db.Column(db.String(10), nullable=False)
    diet_type = db.Column(db.String(10), nullable=False)
    allergies = db.Column(db.Text, nullable=True)
    health_conditions = db.Column(db.Text, nullable=True)
    fitness_goals = db.Column(db.Text, nullable=True)
    dietary_restrictions = db.Column(db.Text, nullable=True)


class DietDiary(db.Model):
    __tablename__ = 'diet_diary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    meals = db.Column(db.Text, nullable=True)
    views = db.Column(db.BigInteger, nullable=True, default=0)
    created_time = db.Column(db.BigInteger, nullable=False)
    # 关联关系
    user = db.relationship('User', backref=db.backref('diet_diaries'))

    def __repr__(self):
        return f'<DietDiary {self.id}>'
