# coding=utf-8

import datetime as dt
from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

# User和Role的关联表
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('roles.id')))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)  # 角色名称
    description = db.Column(db.String(255))  # 角色描述

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))

    regist_time = db.Column(
        db.DateTime, nullable=False, default=dt.datetime.utcnow)  # 注册时间
    last_login_time = db.Column(db.DateTime)  # 上次登录时间
    last_login_ip = db.Column(db.String(32), nullable=True)  # 上次登录IP
    current_login_ip = db.Column(db.String(32), nullable=True)  # 当前登录IP

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """生成token"""
        s = Serializer(current_app.config["SECRET_KEY"], expiration)

        # 把 id、username、roles 放进 token
        token = s.dumps({
            "id": self.id,
            "username": self.username,
            "roles": [role.name for role in self.roles]
        }).decode()
        return token

    @staticmethod
    def confirm(token):
        """验证token"""
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None

        return data
