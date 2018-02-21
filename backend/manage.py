#!/usr/bin/env python
# coding=utf-8

import os
from fabric.api import *
from fabric.contrib.console import confirm
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    from app.api_user.models import User, Role
    return dict(app=app, db=db, User=User, Role=Role)


# manager.add_command("runserver", Server(host="0.0.0.0", port=5000))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)  # 数据库管理
manager.add_command("clean", Clean())  # 清理缓存文件
manager.add_command("url", ShowUrls())  # 打印所有URL


@manager.command
def db_createfirst():
    """首次新建数据库"""
    ret = confirm("drop the database?")
    if ret in ('y', 'Y', "yes"):
        db.drop_all()
        print("drop finish!")
    db.create_all()
    print("The database is created successfully!")
    createsuperuser()


def createrole(name="admin"):
    """创建Role"""
    from app.api_user.models import Role
    # 查看 <name> 角色是否存在
    admin = Role.query.filter_by(name=name).first()
    # 如果没有，则创建角色
    if not admin:
        admin = Role()
        admin.name = name
        db.session.add(admin)
        db.session.commit()
        print("The '%s' role is created!" % name)
    return admin


@manager.command
def createsuperuser():
    """创建超级管理员"""
    from app.api_user.models import User

    admin = createrole()

    username = input("Please Enter the superuser username:")
    if not username:
        print("username is empty!")
        return

    if User.query.filter_by(username=username).first():
        print("There is the same superuser username!")
        return

    password = input("Password:")
    password2 = input("Confirm password:")
    if password != password2:
        print("password is not confirmed!")
        return

    # 创建管理员
    # user_datastore.create_user(username=username, password=password)
    user = User()
    user.username = username
    user.password = password
    user.roles = [admin]
    db.session.add(user)

    db.session.commit()

    print("Superuser is created successfully!")


@manager.command
def test():
    """run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
