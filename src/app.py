# coding=utf8

from flask import Flask
from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy


# 创建应用
app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 2
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.sqlite'
app.config['SECRET_KEY'] = "wotaonihouzi"
app.config['JSON_AS_ASCII'] = False

# 创建数据库
db = SQLAlchemy(app)

# 创建swagger
from src.config import template
Swagger(app, template=template)

# 外部引入
from src.view import main
from src.restapi import api_bp

app.register_blueprint(main)# 不加url_prefix='/auth'，默认是主路径
app.register_blueprint(api_bp)


if __name__ == "__main__":
    app.run(debug=True)
