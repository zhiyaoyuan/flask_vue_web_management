#!/usr/bin/env python
# coding=utf-8

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from config import config

db = SQLAlchemy()

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
# Our API url (can of course be a local resource)
API_URL = 'http://127.0.0.1:5000/spec'

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Flask HTTP API App"
    },
    # oauth_config={ # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    # 'clientId': "your-client-id",
    # 'clientSecret': "your-client-secret-if-required",
    # 'realm': "your-realms",
    # 'appName': "your-app-name",
    # 'scopeSeparator': " ",
    # 'additionalQueryStringParams': {'test': "hello"}
    # }
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    db.app = app

    # 解决禁止跨域请求的问题
    CORS(app)

    # 注册蓝本
    # 增加 api 蓝本
    from app.api_user import api_user
    app.register_blueprint(api_user, url_prefix='/api/user')

    # 附加路由和自定义的错误页面

    # swagger API文档
    swag = swagger(app, from_file_keyword="swagger_from_file")
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Flask HTTP API"

    def spec():
        return jsonify(swag)

    app.add_url_rule('/spec', view_func=spec)
    # Register blueprint at URL
    # (URL must match the one given to factory function above)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    return app
