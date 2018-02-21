#!/usr/bin/env python
# coding=utf-8

from flask import jsonify
from . import api_user


@api_user.app_errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "404 Not Found!"}), 404


@api_user.app_errorhandler(500)
def internal_server_error(e):
    return jsonify({"status": 500, "message": "500 Server Error!"}), 500
