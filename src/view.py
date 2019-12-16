import json
from flask import jsonify, request, redirect, g, Blueprint
from src.db_modle.userobj import User, UserInfo, db
from src.authcc import token_auth, auth

main = Blueprint('main', __name__)


#  注册
@main.route('/register', methods=['POST'])
def new_user():
    """
    注册用户
    这就是里面的具体说明啦，用户名最长32位，密码最长128
    It works also with swag_from, schemas and spec_dict
    ---
    tags:
      - 用户
    parameters:
      - in: "body"
        name: "body"
        description: " 这是注册用户body的描述"
        required: true
        schema:
          $ref: "#/definitions/user"
    definitions:
      user:
        type: "object"
        required:
          - "username"
          - "password"
        properties:
          username:
            type: "string"
            example: "houzi"
          password:
            type: "string"
            example: "123456"
    responses:
      200:
        description: "成功"
      201:
        description: "Invalid user supplied"
      202:
        description: "User existing"
    """
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({'code': 201, 'msg': "missing arguments"}), 201  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'code': 202, 'msg': "existing user"}), 202  # existing user
    user = User(username=username, status="normal")
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    # 用户信息+ token
    user = User.query.filter_by(username=username).first()
    token = str(user.generate_auth_token(), encoding="utf8")
    return jsonify({'code': 200, 'msg': "success", 'data': {'username': user.username, 'token': token}}), 200


#  获取用户资源
@main.route('/get_userinfo', methods=['GET'])
@token_auth.login_required
def get_userinfo():
    """
    获取用户的信息
    It works also with swag_from, schemas and spec_dict
    ---
    tags:
      - 用户
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
    responses:
      200:
        description: "成功"
      201:
        description: "arguments is not none"
    """
    user_id = g.user.id
    if user_id is None:
        return jsonify({'code': 201, 'msg': "userid is none"}), 201  # missing arguments
    user = User.query.filter_by(id=user_id).first()
    userinfolist = user.userinfo
    if userinfolist:
        userinfo = userinfolist[0]
        data = {'username': user.username, 'status':user.status,'remark': userinfo.remark, 'age': userinfo.age,
                "email": userinfo.email}
    else:
        data = {'username': user.username, 'status': user.status}
    return jsonify({'code': 200, 'msg': "success", 'data': data})


#  更改用互信息
@main.route('/adit_userinfo', methods=['POST'])
@token_auth.login_required
def adit_userinfo():
    """
    注册用户
    这就是里面的具体说明啦，用户名最长32位，密码最长128
    It works also with swag_from, schemas and spec_dict
    ---
    tags:
      - 用户
    parameters:
      - in: header
        name: Authorization
        type: string
        required: true
      - in: "body"
        name: "body"
        description: " 这是注册用户body的描述"
        required: true
        schema:
          $ref: "#/definitions/adituser"
    definitions:
      adituser:
        type: "object"
        required:
          - "age"
          - "remark"
          - "email"
        properties:
          age:
            type: "int"
            example: 18
          remark:
            type: "string"
            example: "mark 你是个标签"
          email:
            type: "string"
            example: "123@qq.com"
    responses:
      200:
        description: "成功"
      201:
        description: "修改失败"
    """
    user_id = g.user.id
    reqdata = request.json
    data = {}
    if reqdata:
        userinfo = UserInfo.query.filter_by(userid=user_id).first()
        if userinfo:
            userinfo.age = reqdata.get("age")
            userinfo.remark = reqdata.get("remark")
            userinfo.email = reqdata.get("email")
        else:
            userinfo = UserInfo()
            userinfo.age = reqdata.get("age")
            userinfo.remark = reqdata.get("remark")
            userinfo.email = reqdata.get("email")
            userinfo.userid = user_id
            db.session.add(userinfo)
        db.session.commit()
        data = {'username': g.user.username, 'remark': userinfo.remark, 'age': userinfo.age, "email": userinfo.email}

    return jsonify({'code': 200, 'msg': "success", 'data': data})


#  登录
@main.route('/login', methods=['POST'])
@auth.login_required
def get_auth_token():
    """
    用户登录
    这就是里面的具体说明啦，用户名最长32位，密码最长128
    It works also with swag_from, schemas and spec_dict
    ---
    tags:
      - 用户
    parameters:
      - in: "body"
        name: "body"
        description: " 这是注册用户body的描述"
        required: true
        schema:
          $ref: "#/definitions/user"
    definitions:
      user:
        type: "object"
        required:
          - "username"
          - "password"
        properties:
          username:
            type: "string"
            example: "houzi"
          password:
            type: "string"
            example: "123456"
    responses:
      201:
        description: "Invalid user supplied"
      202:
        description: "password or user error"
    """
    token = g.user.generate_auth_token()
    userinfolist = g.user.userinfo

    if userinfolist:
        userinfo =userinfolist[0]
        data = jsonify({'code': 200, 'msg': "login success!",
                        'data': {'username': g.user.username, 'remark': userinfo.remark,
                                 'age': userinfo.age, "email": userinfo.email,
                                 'token': str(token, encoding="utf8")}})
    else:
        data = jsonify({'code': 200, 'msg': "login success!",
                        'data': {'username': g.user.username, 'status': g.user.status,
                                 'token': str(token, encoding="utf8")}})
    return data, 200


@main.route('/')
def hello_world():
    return redirect("/apidocs")


@main.route('/colors/<palette>')
def colors(palette):
    """
    这个是接口的外层说明
    这个是接口展开的详细说明:zheli写很详细的而说宁
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
      404:
        description: '找不到路由'
    """
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)
