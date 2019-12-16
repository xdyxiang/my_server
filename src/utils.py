# 初始化数据库

from src.app import db

def createdb():
    db.create_all()


def dropdb():
    db.drop_all()


createdb()
# dropdb()
