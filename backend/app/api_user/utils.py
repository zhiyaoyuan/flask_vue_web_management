#!/usr/bin/env python
# coding=utf-8

from functools import wraps
from flask import request, jsonify, current_app
from .models import User


class Status():
    class SUCCESS:
        status = 1
        message = "success!"

    class FAIL:
        status = 0
        message = "fail!"

    class PARAMETER_ERROR:
        status = -1
        message = "Parameter Error!"

    class TOKEN_ERROR:
        status = -2
        message = "Token Error!"

    class FORBIDDEN:
        status = 403
        message = "Forbidden!"


def confirm_token(allow_roles: list = None):
    def wrap_function(func):
        """装饰器：验证token和角色权限

        @parameter: roles - 许可的角色list

        使用方法：
        ```
        @confirm_token()
        def function():
            pass
        
        @conconfirm_token(["admin"])
        def function():
            pass
        ```
        """

        @wraps(func)
        def decorated_view(*args, **kwargs):
            # TODO:
            ret_json = {
                "status": Status.TOKEN_ERROR.status,
                "message": Status.TOKEN_ERROR.message,
                "request": request.base_url,
                "data": {}
            }
            token = request.values.get("token")
            if not token:
                ret_json.update({
                    "status": Status.PARAMETER_ERROR.status,
                    "message": Status.PARAMETER_ERROR.message
                })
                return jsonify(ret_json)  # return fail

            data = User.confirm(token)
            if not data:
                return jsonify(ret_json)  # return fail

            # 如果需要进行权限判断
            if allow_roles:
                token_roles = data.get("roles")
                # print("token_roles:", token_roles)
                allow = set(allow_roles) & set(token_roles)
                print("allow:", allow)
                if not allow:
                    ret_json.update({
                        "status": Status.FORBIDDEN.status,
                        "message": Status.FORBIDDEN.message
                    })
                    return jsonify(ret_json)  # return fail

            # 成功返回
            return func(*args, **kwargs)

        return decorated_view

    return wrap_function


def confirm_key(keys: list):
    """装饰器：验证请求参数

    使用方式：
    @confirm_key(["token"])
    def confirm_token():
        pass
    """

    def wrap_function(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # TODO:
            ret_json = {
                "status": Status.PARAMETER_ERROR.status,
                "message": Status.PARAMETER_ERROR.message,
                "request": request.base_url,
                "data": {}
            }
            # 要设置 Content-Type: multipart/form-data 头才能获取得到
            values = request.values
            # print(values)
            for key in keys:
                if not values.get(key):
                    return jsonify(ret_json)

            return func(*args, **kwargs)

        return decorated_view

    return wrap_function
