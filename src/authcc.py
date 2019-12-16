# coding=utf8

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask import jsonify, request, g
from src.db_modle.userobj import User
from src.app import app,db


# 认证账户名和密码
auth = HTTPBasicAuth()
# 认证token
token_auth = HTTPTokenAuth()


@auth.verify_password
def verify_password(username, password):
    # 如果是从登录接口过来的，验证用户密码
    username = request.json.get("username")
    password = request.json.get("password")
    if username!=None and password!=None:
        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return False
        g.user = user
        return True
    return False

@auth.error_handler
def unauthorized():
    return jsonify({'code': '403', 'msg': '账户名或者密码错误'})


@token_auth.verify_token
def verify_token(t):
    token = request.headers.get("Authorization")
    if token:
        status,user = User.verify_auth_token(token)
        if status:
            g.user = user
            return True
        else:
            return False
    return False


@token_auth.error_handler
def unauthorized():
    return jsonify({'code': '401', 'msg': 'token认证失败'})



@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Redirect"] = "*"
    return response

@app.before_first_request
def init_db():
    db.create_all()
